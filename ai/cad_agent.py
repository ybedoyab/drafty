from crewai import Agent
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class CADAgent(Agent):
    """Agent that converts natural language description to CAD script."""

    def __init__(self, model_name: str = "thirteen3333/text2cad-multiturn"):
        super().__init__(
            name="CADAgent",
            role="CAD Modeling Expert",
            goal="Convert detailed geometric descriptions into precise CAD scripts for 3D modeling",
            backstory="You are a senior CAD engineer with expertise in parametric modeling, OpenSCAD, and engineering design. You understand complex geometric relationships and can translate descriptions into accurate CAD code."
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        ).to("cuda" if torch.cuda.is_available() else "cpu")

    def run(self, description: str, max_new_tokens: int = 200) -> str:
        prompt = (
            "You are an expert CAD modeler. Write a parametric OpenSCAD script for "
            "the following object, including dimensions, key geometries and constraints.\n"+
            description
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        return self.tokenizer.decode(out[0], skip_special_tokens=True) 