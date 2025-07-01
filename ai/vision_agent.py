from crewai import Agent
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class VisionAgent(Agent):
    """Agent that produces a descriptive caption for an input image."""

    def __init__(self, device: str | None = None):
        super().__init__(name="VisionAgent")
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)

    def run(self, image_path: str, task_description: str = "Describe the geometry") -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt").to(self.device)
        
        # Use the task description as a prompt prefix if provided
        if task_description and "User provided additional context" in task_description:
            # Extract user description from the task
            import re
            user_context_match = re.search(r"User provided additional context: (.+?)\.", task_description)
            if user_context_match:
                user_context = user_context_match.group(1)
                # Create a more specific prompt
                prompt = f"Describe this 3D object in detail for CAD modeling. Consider: {user_context}. Focus on dimensions, geometry, and engineering specifications."
            else:
                prompt = "Describe this 3D object in detail for CAD modeling, focusing on dimensions and geometry."
        else:
            prompt = "Describe this 3D object in detail for CAD modeling, focusing on dimensions and geometry."
        
        inputs = self.processor(image, text=prompt, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_new_tokens=128)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption 