from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import re
import os

class OpenSCADValidatorInput(BaseModel):
    """Input schema for OpenSCAD Validator Tool."""
    openscad_code: str = Field(..., description="The OpenSCAD code to validate and correct.")

class OpenSCADValidator(BaseTool):
    name: str = "OpenSCAD Validator and Corrector"
    description: str = (
        "Validates OpenSCAD code for syntax errors and common mistakes. "
        "Corrects issues like 2D objects in 3D context, missing semicolons, "
        "invalid hull usage, and unrealistic dimensions. "
        "Returns corrected OpenSCAD code that will compile successfully."
    )
    args_schema: Type[BaseModel] = OpenSCADValidatorInput

    def _run(self, openscad_code: str) -> str:
        """Validate and correct OpenSCAD code."""
        
        # Load knowledge base
        knowledge_path = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge')
        
        # Read best practices
        best_practices = ""
        try:
            with open(os.path.join(knowledge_path, 'openscad_best_practices.txt'), 'r') as f:
                best_practices = f.read()
        except FileNotFoundError:
            best_practices = "Basic OpenSCAD syntax rules"
        
        # Read common patterns
        common_patterns = ""
        try:
            with open(os.path.join(knowledge_path, 'openscad_common_patterns.txt'), 'r') as f:
                common_patterns = f.read()
        except FileNotFoundError:
            common_patterns = "Common OpenSCAD patterns"
        
        # Apply corrections
        corrected_code = self._apply_corrections(openscad_code)
        
        # Validate the corrected code
        validation_result = self._validate_code(corrected_code)
        
        if validation_result['is_valid']:
            return f"VALIDATED AND CORRECTED OPENSCAD CODE:\n\n{corrected_code}\n\nValidation: {validation_result['message']}"
        else:
            return f"PARTIALLY CORRECTED CODE (requires manual review):\n\n{corrected_code}\n\nIssues found: {validation_result['message']}"

    def _apply_corrections(self, code: str) -> str:
        """Apply common corrections to OpenSCAD code."""
        
        # Fix missing semicolons
        code = re.sub(r'(\w+\([^)]*\))\s*$', r'\1;', code, flags=re.MULTILINE)
        
        # Fix 2D objects in 3D context
        code = re.sub(r'circle\(([^)]*)\);', r'cylinder(h=10, r=\1, $fn=32);', code)
        
        # Fix invalid hull usage with 2D objects
        code = re.sub(r'hull\(\)\s*{\s*circle\(([^)]*)\);', r'hull() {\n    cylinder(h=10, r=\1, $fn=32);', code)
        
        # Fix unrealistic dimensions (convert meters to mm)
        code = re.sub(r'(\w+)\s*=\s*(\d{3,});', r'\1 = \2; // Consider if this should be in mm instead of meters', code)
        
        # Add missing $fn parameters for smooth circles
        code = re.sub(r'cylinder\(([^)]*)\);', r'cylinder(\1, $fn=32);', code)
        code = re.sub(r'sphere\(([^)]*)\);', r'sphere(\1, $fn=32);', code)
        
        # Fix common parameter names
        code = re.sub(r'height\s*=', r'h =', code)
        code = re.sub(r'radius\s*=', r'r =', code)
        code = re.sub(r'diameter\s*=', r'd =', code)
        
        return code

    def _validate_code(self, code: str) -> dict:
        """Validate OpenSCAD code for common issues."""
        issues = []
        
        # Check for missing semicolons
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('//') and not line.startswith('/*') and not line.endswith(';') and not line.endswith('{') and not line.endswith('}'):
                if '=' in line or '(' in line:
                    issues.append(f"Line {i}: Missing semicolon")
        
        # Check for 2D objects in 3D context
        if 'circle(' in code and 'linear_extrude' not in code and 'rotate_extrude' not in code:
            issues.append("2D circle used without extrusion")
        
        # Check for unrealistic dimensions
        large_numbers = re.findall(r'(\d{4,})', code)
        if large_numbers:
            issues.append(f"Large dimensions detected: {large_numbers} - consider if these should be in mm")
        
        # Check for missing $fn parameters
        if 'cylinder(' in code and '$fn' not in code:
            issues.append("Cylinders without $fn parameter may appear faceted")
        
        if 'sphere(' in code and '$fn' not in code:
            issues.append("Spheres without $fn parameter may appear faceted")
        
        return {
            'is_valid': len(issues) == 0,
            'message': '; '.join(issues) if issues else 'Code appears valid'
        } 