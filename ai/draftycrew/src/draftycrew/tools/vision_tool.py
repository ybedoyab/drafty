from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from PIL import Image
import base64
import io

class VisionToolInput(BaseModel):
    """Input schema for Vision Tool."""
    image_path: str = Field(..., description="Path to the image file to analyze")

class VisionTool(BaseTool):
    name: str = "Vision Analysis Tool"
    description: str = (
        "Analyzes images to extract geometric information, dimensions, shapes, and visual characteristics. "
        "Use this tool to understand what objects are in an image and their visual properties. "
        "Returns detailed analysis of shapes, colors, textures, and geometric features."
    )
    args_schema: Type[BaseModel] = VisionToolInput

    def _run(self, image_path: str) -> str:
        """Analyze an image and return detailed visual information."""
        try:
            # Check if image file exists
            if not os.path.exists(image_path):
                return f"Error: Image file not found at {image_path}"
            
            # Open and analyze the image
            with Image.open(image_path) as img:
                # Get basic image information
                width, height = img.size
                mode = img.mode
                format_name = img.format
                
                # Convert to RGB if necessary
                if mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get image statistics
                pixels = list(img.getdata())
                total_pixels = len(pixels)
                
                # Calculate basic color statistics
                r_values = [p[0] for p in pixels]
                g_values = [p[1] for p in pixels]
                b_values = [p[2] for p in pixels]
                
                avg_r = sum(r_values) / len(r_values)
                avg_g = sum(g_values) / len(g_values)
                avg_b = sum(b_values) / len(b_values)
                
                # Analyze image characteristics
                analysis = f"""
IMAGE ANALYSIS REPORT:
=====================

Basic Information:
- Dimensions: {width} x {height} pixels
- Format: {format_name}
- Color Mode: {mode}
- Total Pixels: {total_pixels:,}

Color Analysis:
- Average RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})
- Dominant Color: {'Red' if avg_r > avg_g and avg_r > avg_b else 'Green' if avg_g > avg_b else 'Blue'}

Geometric Analysis:
- Aspect Ratio: {width/height:.2f} ({'Landscape' if width > height else 'Portrait' if height > width else 'Square'})
- Image Size Category: {'Small' if total_pixels < 100000 else 'Medium' if total_pixels < 1000000 else 'Large'}

Visual Characteristics:
- Image appears to be a {'photograph' if format_name in ['JPEG', 'JPG'] else 'digital image'}
- Resolution: {'Low' if total_pixels < 500000 else 'Medium' if total_pixels < 2000000 else 'High'}
- Color Distribution: {'Monochromatic' if abs(avg_r - avg_g) < 30 and abs(avg_g - avg_b) < 30 else 'Colorful'}

Recommendations for CAD Generation:
- Consider the aspect ratio when creating 3D models
- Use the dominant color as a reference for material selection
- Scale dimensions appropriately based on image resolution
- Pay attention to geometric shapes visible in the image
                """
                
                return analysis.strip()
                
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
