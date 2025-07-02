from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

class OpenSCADKnowledgeInput(BaseModel):
    """Input schema for OpenSCAD Knowledge Tool."""
    query: str = Field(..., description="Query about OpenSCAD best practices, patterns, or syntax.")

class OpenSCADKnowledgeTool(BaseTool):
    name: str = "OpenSCAD Knowledge Base"
    description: str = (
        "Provides OpenSCAD best practices, syntax rules, common patterns, and templates. "
        "Use this tool to get guidance on proper OpenSCAD code structure, common mistakes to avoid, "
        "and templates for different object types like furniture, mechanical parts, etc."
    )
    args_schema: Type[BaseModel] = OpenSCADKnowledgeInput

    def _run(self, query: str) -> str:
        """Provide OpenSCAD knowledge based on the query."""
        
        # Load knowledge base files
        knowledge_path = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge')
        
        best_practices = ""
        common_patterns = ""
        
        try:
            with open(os.path.join(knowledge_path, 'openscad_best_practices.txt'), 'r') as f:
                best_practices = f.read()
        except FileNotFoundError:
            best_practices = "Best practices file not found"
        
        try:
            with open(os.path.join(knowledge_path, 'openscad_common_patterns.txt'), 'r') as f:
                common_patterns = f.read()
        except FileNotFoundError:
            common_patterns = "Common patterns file not found"
        
        # Combine knowledge
        full_knowledge = f"""
OPENSCAD KNOWLEDGE BASE
=======================

BEST PRACTICES:
{best_practices}

COMMON PATTERNS AND TEMPLATES:
{common_patterns}

QUERY: {query}

BASED ON YOUR QUERY, HERE ARE THE RELEVANT GUIDELINES:

"""
        
        # Provide specific guidance based on query
        query_lower = query.lower()
        
        if 'furniture' in query_lower or 'chair' in query_lower or 'table' in query_lower:
            full_knowledge += """
FURNITURE-SPECIFIC GUIDELINES:
- Use realistic dimensions: 400-500mm width, 400-500mm depth, 800-900mm height
- Leg diameters: 20-50mm for stability
- Seat height: 400-500mm from ground
- Backrest angle: 5-15 degrees from vertical
- Use parametric variables for easy modification
"""
        
        if 'syntax' in query_lower or 'error' in query_lower:
            full_knowledge += """
SYNTAX AND ERROR PREVENTION:
- All statements must end with semicolon (;)
- 2D shapes (circle, square) must be extruded to become 3D
- Use cylinder() instead of circle() in 3D context
- Add $fn=32 or higher for smooth circular objects
- Check that all dimensions are positive numbers
"""
        
        if 'dimensions' in query_lower or 'scale' in query_lower:
            full_knowledge += """
DIMENSION GUIDELINES:
- Use millimeters (mm) for most objects
- Avoid dimensions over 1000mm unless specifically needed
- Typical furniture dimensions: 400-800mm
- Use parametric variables: length = 400; width = length * 0.8;
"""
        
        if 'validation' in query_lower or 'check' in query_lower:
            full_knowledge += """
VALIDATION CHECKLIST:
- All statements end with semicolon
- No 2D objects in 3D context without extrusion
- All dimensions are positive numbers
- Cylinders and spheres have $fn parameter
- Boolean operations are valid
- Transformations don't create degenerate geometry
"""
        
        return full_knowledge 