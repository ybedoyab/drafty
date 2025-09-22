"""AI orchestrator: runs vision analysis and generates OpenSCAD via ModelArts."""
import os
import sys
from pathlib import Path
import shutil
from typing import Dict, Any
import uuid
import requests
from crewai import Crew, Process

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
    """Call Huawei ModelArts to produce only OpenSCAD code from a description."""
    cfg_path = Path(__file__).parent / "config" / "system_prompt.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    system_prompt = cfg.get("openscad_generator", {}).get("system", "")
    kb = _load_openscad_knowledge()
    if kb:
        system_prompt = f"{system_prompt}\n\nFollow these brief OpenSCAD best-practices:\n{kb}"
    template = cfg.get("openscad_generator", {}).get("template", "")
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
    """Sanitize LLM output to return pure OpenSCAD code (no fences or <think>)."""
    if not raw_text:
        return ""
    text = raw_text
    while True:
        start = text.find("<think>")
        end = text.find("</think>")
        if start != -1 and end != -1 and end > start:
            text = text[:start] + text[end + len("</think>") :]
        else:
            break
    text = text.replace("```openscad", "").replace("```OpenSCAD", "").replace("```", "")
    return text.strip()


def run_pipeline(image_path: str, description: str = None) -> Dict[str, Any]:
    """Run vision analysis and generate OpenSCAD; return script and metadata."""
    try:
        ai_root = Path(__file__).parent
        imagen_dir = ai_root / "imagen"
        outputs_dir = ai_root / "generated_scad"
        outputs_dir.mkdir(exist_ok=True)
        imagen_dir.mkdir(exist_ok=True)
        
        if image_path.startswith('http'):
            image_base = Path(image_path.split('/')[-1]).stem
        else:
            image_base = Path(image_path).stem
        unique_id = str(uuid.uuid4())[:8]
        cad_script_filename = f"{image_base}_{unique_id}_cad.scad"
        cad_script_path = outputs_dir / cad_script_filename
        
        target_image_path = imagen_dir / "ejemplo_drafty.jpg"
        
        if image_path.startswith('http'):
            response = requests.get(image_path, timeout=30)
            response.raise_for_status()
            with open(target_image_path, 'wb') as f:
                f.write(response.content)
        else:
            shutil.copy2(image_path, target_image_path)
        
        inputs = {
            'image_path': str(target_image_path),
            'cad_script_path': str(cad_script_path)
        }
        
        if description:
            inputs['description'] = description
        
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

        tech_description = str(vision_result) if vision_result is not None else ""
        if description:
            tech_description = f"{tech_description}\n\nUser notes:\n{description}"

        cad_script_raw = _call_modelarts_for_openscad(tech_description)
        cad_script = _clean_openscad_output(cad_script_raw)
        
        if cad_script:
            with open(cad_script_path, 'w', encoding='utf-8') as f:
                f.write(cad_script)
        
        return {
            "cad_script": cad_script,
            "cad_script_filename": cad_script_filename,
            "vision_result": tech_description
        }
        
    except Exception as e:
        raise Exception(f"Error in AI pipeline: {str(e)}") 