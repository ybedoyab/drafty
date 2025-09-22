#!/usr/bin/env python
"""
AI Module Entry Point

This module provides the main entry point for the AI system.
The AI module is designed to be called by the backend orchestrator,
not run independently with hardcoded paths.
"""

import sys
import warnings
from pathlib import Path

# Add the ai directory to Python path
ai_path = Path(__file__).parent
sys.path.append(str(ai_path))

from crew import Draftycrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run_with_image(image_path: str):
    """
    Run the crew with a provided image path.
    
    Args:
        image_path (str): Path to the image file to process
        
    Returns:
        dict: Results from the crew execution
    """
    inputs = {
        'image_path': image_path
    }
    try:
        result = Draftycrew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    print("AI Module - This should be called by the backend orchestrator")
    print("For testing purposes, you can provide an image path as argument")
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"Processing image: {image_path}")
        result = run_with_image(image_path)
        print("Processing completed successfully")
    else:
        print("Usage: python main.py <image_path>")
        print("Example: python main.py /path/to/image.jpg")
