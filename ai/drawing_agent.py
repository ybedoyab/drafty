from crewai import Agent
import ezdxf
from pathlib import Path

class DrawingAgent(Agent):
    """Agent that converts a CAD script into a simple DXF drawing with dimensions."""

    def __init__(self):
        super().__init__(
            name="DrawingAgent",
            role="Engineering Drawing Specialist",
            goal="Convert CAD scripts into professional 2D engineering drawings with proper dimensions and annotations",
            backstory="You are a certified engineering drafter with extensive experience in creating technical drawings, dimensioning, and CAD-to-DXF conversion. You ensure drawings meet industry standards."
        )

    def run(self, cad_script: str, output_path: str | None = None):
        # In a full implementation, parse cad_script and generate 2D projection.
        # For hackathon prototype we create a placeholder DXF with the script embedded as comment.
        output_path = output_path or "output.dxf"
        doc = ezdxf.new(setup=True)
        msp = doc.modelspace()
        # Add script as text in DXF so reviewers can see it
        msp.add_text("CAD Script:").set_pos((0, 0))
        msp.add_text(cad_script, dxfattribs={"height": 0.25}).set_pos((0, -0.5))
        doc.saveas(output_path)
        return str(Path(output_path).resolve()) 