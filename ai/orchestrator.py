from crewai import Crew, Task
from .vision_agent import VisionAgent
from .cad_agent import CADAgent
from .drawing_agent import DrawingAgent

def run_pipeline(image_path: str, user_description: str = None) -> dict:
    """Execute the crew pipeline and return the generated DXF file path and CAD script."""
    
    # Create agents dynamically to avoid initialization issues
    vision_agent = VisionAgent()
    cad_agent = CADAgent()
    drawing_agent = DrawingAgent()
    
    # Define tasks
    caption_task = Task(agent=vision_agent, description="Describe the geometry", output_key="description")
    cad_task = Task(agent=cad_agent, description="{description}", output_key="cad_script")
    drawing_task = Task(agent=drawing_agent, description="{cad_script}", output_key="dxf_file")
    
    # If user provided description, use it to enhance the vision agent's output
    if user_description:
        # Modify the vision task to include user description
        enhanced_caption_task = Task(
            agent=vision_agent, 
            description=f"Describe the geometry in the image. User provided additional context: {user_description}. Use this information to enhance your description with specific dimensions and details.",
            output_key="description"
        )
        crew = Crew(tasks=[enhanced_caption_task, cad_task, drawing_task])
    else:
        crew = Crew(tasks=[caption_task, cad_task, drawing_task])
    
    result = crew.run(initial_input=image_path)
    
    return {
        "dxf_file": result["dxf_file"],
        "cad_script": result["cad_script"]
    } 