import os
import sys
from pathlib import Path
import shutil
from typing import Dict, Any
import uuid
from crewai import Crew, Process

# Add the draftycrew src directory to Python path
draftycrew_src_path = Path(__file__).parent / "draftycrew" / "src"
sys.path.append(str(draftycrew_src_path))

from draftycrew.crew import Draftycrew

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
        # Copy the uploaded image to the draftycrew imagen directory
        draftycrew_root = Path(__file__).parent / "draftycrew"
        imagen_dir = draftycrew_root / "imagen"
        imagen_dir.mkdir(exist_ok=True)
        
        # Generate a unique name for the CAD script based on the uploaded image
        image_base = Path(image_path).stem
        unique_id = str(uuid.uuid4())[:8]
        cad_script_filename = f"{image_base}_{unique_id}_cad.scad"
        cad_script_path = draftycrew_root / cad_script_filename
        
        # Copy the image to the expected location (for vision tool)
        target_image_path = imagen_dir / "ejemplo_drafty.jpg"
        shutil.copy2(image_path, target_image_path)
        
        # Create inputs for the crew
        inputs = {
            'image_path': str(target_image_path),
            'cad_script_path': str(cad_script_path)
        }
        
        if description:
            inputs['description'] = description
        
        # Run the CrewAI pipeline with custom output file
        crew = Draftycrew()
        analyze_task = crew.analyze_image()
        generate_task = crew.generate_cad_task(str(cad_script_path))
        agents = [crew.visualizer(), crew.cad_generator()]
        tasks = [analyze_task, generate_task]
        crew_instance = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        result = crew_instance.kickoff(inputs=inputs)
        
        # Read the generated CAD script
        cad_script = ""
        
        if cad_script_path.exists():
            with open(cad_script_path, 'r', encoding='utf-8') as f:
                cad_script = f.read()
        
        # Return the results
        return {
            "cad_script": cad_script,
            "cad_script_filename": cad_script_filename,
            "result": result
        }
        
    except Exception as e:
        raise Exception(f"Error in AI pipeline: {str(e)}") 