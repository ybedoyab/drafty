import os
import sys
from pathlib import Path
import shutil
from typing import Dict, Any
import uuid
import requests
from crewai import Crew, Process

# Add the ai directory to Python path
ai_path = Path(__file__).parent
sys.path.append(str(ai_path))

from crew import Draftycrew
from llm_wrapper import huawei_llm_wrapper
from ai.config import settings
import json


def _load_openscad_knowledge() -> str:
    """Summarize OpenSCAD knowledge files to keep prompts small."""
    base = Path(__file__).parent / "knowledge"
    texts = []
    for name in ["openscad_best_practices.txt", "openscad_common_patterns.txt", "user_preference.txt"]:
        p = base / name
        if p.exists():
            try:
                texts.append(p.read_text(encoding="utf-8"))
            except Exception:
                continue
    full = "\n\n".join(texts)
    if not full:
        return ""
    # Lightweight heuristic summarization: keep headings and bullet lines
    lines = full.splitlines()
    kept = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith(('- ', '* ', '#', '– ')) or ':' in s or '()' in s or '_' in s or 'OpenSCAD' in s:
            kept.append(s)
        if len(kept) >= settings.KNOWLEDGE_SUMMARY_MAX_LINES:
            break
    return "\n".join(kept)

def _call_modelarts_for_openscad(tech_description: str) -> str:
    """Call Huawei ModelArts (DeepSeek) to produce ONLY OpenSCAD code from a technical description."""
    # Load system prompt from config JSON
    cfg_path = Path(__file__).parent / "config" / "system_prompt.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    system_prompt = cfg.get("openscad_generator", {}).get("system", "")
    kb = _load_openscad_knowledge()
    if kb:
        system_prompt = f"{system_prompt}\n\nFollow these brief OpenSCAD best-practices:\n{kb}"
    template = cfg.get("openscad_generator", {}).get("template", "")
    # Send a single user message (some endpoints reject system role). Include rules + template + description
    # Truncate the technical description to keep under model context
    safe_description = tech_description[:settings.MAX_DESCRIPTION_CHARS]

    combined_prompt = (
        f"{system_prompt}\n\n"
        "Generate pure OpenSCAD that accurately models the object.\n"
        "Follow the rules above. Use variables for dimensions; do not store shapes in variables.\n"
        "Output code only.\n\n"
        f"{template}\n"
        f"Technical Description:\n{safe_description}\n"
    )
    from langchain_core.messages import HumanMessage
    result = huawei_llm_wrapper._generate([
        HumanMessage(content=combined_prompt),
    ], max_tokens=settings.DEFAULT_MAX_TOKENS)
    return result.generations[0][0].text if result and result.generations else ""


def _clean_openscad_output(raw_text: str) -> str:
    """Sanitize LLM output to return ONLY pure OpenSCAD code.

    - Removes DeepSeek/Huawei <think>...</think> traces
    - Strips markdown code fences (``` and language hints)
    - Trims whitespace
    """
    if not raw_text:
        return ""
    text = raw_text
    # Remove <think> blocks
    while True:
        start = text.find("<think>")
        end = text.find("</think>")
        if start != -1 and end != -1 and end > start:
            text = text[:start] + text[end + len("</think>") :]
        else:
            break
    # Strip code fences
    text = text.replace("```openscad", "").replace("```OpenSCAD", "").replace("```", "")
    # Final trim
    return text.strip()


def run_pipeline(image_path: str, description: str = None) -> Dict[str, Any]:
    """
    Run the AI pipeline to generate CAD from an image.
    
    Args:
        image_path: Path to the input image
        description: Optional description for the CAD generation
        
    Returns:
        Dictionary containing the CAD script and metadata
    """
    try:
        # Copy the uploaded image to the ai imagen directory
        ai_root = Path(__file__).parent
        imagen_dir = ai_root / "imagen"
        outputs_dir = ai_root / "generated_scad"
        outputs_dir.mkdir(exist_ok=True)
        imagen_dir.mkdir(exist_ok=True)
        
        # Generate a unique name for the CAD script based on the uploaded image
        if image_path.startswith('http'):
            # Extract filename from URL
            image_base = Path(image_path.split('/')[-1]).stem
        else:
            image_base = Path(image_path).stem
        unique_id = str(uuid.uuid4())[:8]
        cad_script_filename = f"{image_base}_{unique_id}_cad.scad"
        cad_script_path = outputs_dir / cad_script_filename
        
        # Copy the image to the expected location (for vision tool)
        target_image_path = imagen_dir / "ejemplo_drafty.jpg"
        
        # Handle both local file paths and cloud URLs
        if image_path.startswith('http'):
            # Download from cloud storage
            response = requests.get(image_path, timeout=30)
            response.raise_for_status()
            with open(target_image_path, 'wb') as f:
                f.write(response.content)
        else:
            # Copy local file
            shutil.copy2(image_path, target_image_path)
        
        # Create inputs for the crew
        inputs = {
            'image_path': str(target_image_path),
            'cad_script_path': str(cad_script_path)
        }
        
        if description:
            inputs['description'] = description
        
        # 1) Run only the vision analysis via CrewAI (OpenAI), to get the technical description
        crew = Draftycrew()
        analyze_task = crew.analyze_image()
        agents = [crew.visualizer()]
        tasks = [analyze_task]
        crew_instance = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        vision_result = crew_instance.kickoff(inputs=inputs)

        # Extract description text
        tech_description = str(vision_result) if vision_result is not None else ""
        if description:
            tech_description = f"{tech_description}\n\nUser notes:\n{description}"

        # 2) Call Huawei ModelArts (DeepSeek) directly to generate OpenSCAD code
        cad_script_raw = _call_modelarts_for_openscad(tech_description)
        cad_script = _clean_openscad_output(cad_script_raw)
        
        # Persist to file
        if cad_script:
            with open(cad_script_path, 'w', encoding='utf-8') as f:
                f.write(cad_script)
        
        # Return the results
        return {
            "cad_script": cad_script,
            "cad_script_filename": cad_script_filename,
            "vision_result": tech_description
        }
        
    except Exception as e:
        raise Exception(f"Error in AI pipeline: {str(e)}") 