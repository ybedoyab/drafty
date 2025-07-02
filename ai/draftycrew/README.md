# Draftycrew - AI Agents for CAD Generation

This is the CrewAI project component of **Drafty**, an AI-powered CAD generation system. This module contains the specialized AI agents that analyze images and generate OpenSCAD code.

## Overview

Draftycrew uses two AI agents working together:

1. **Visualizer Agent**: Analyzes engineering images and generates precise technical specifications
2. **CAD Generator Agent**: Converts technical descriptions into functional OpenSCAD code using a knowledge base

## Features

### 🤖 AI Agents
- **Image Analysis**: Advanced computer vision for geometric feature extraction
- **Technical Specifications**: Precise dimensional analysis with exact measurements
- **OpenSCAD Generation**: Parametric, compilable CAD code
- **Knowledge Integration**: Best practices and validation tools

### 📚 Knowledge Base System
- **Best Practices**: OpenSCAD syntax rules and guidelines
- **Common Patterns**: Templates for furniture and mechanical parts
- **Validation Tools**: Automatic error detection and correction
- **Realistic Dimensions**: Furniture-specific guidelines

### 🛠️ Custom Tools
- **OpenSCAD Knowledge Tool**: Provides contextual guidance
- **OpenSCAD Validator Tool**: Validates and corrects generated code

## Installation

### Prerequisites
- Python 3.12
- Windows PowerShell (for UV installation)

### Setup Steps

1. **Navigate to AI directory:**
```bash
cd C:\Users\Alejo\Documents\drafty\ai
```

2. **Create virtual environment:**
```bash
py -3.12 --version
py -3.12 -m venv .venv
```

3. **Install UV package manager:**
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

4. **Install CrewAI:**
```bash
uv tool install crewai
```

5. **Navigate to project and install dependencies:**
```bash
cd draftycrew
pip install 'crewai[tools]'
```

6. **Install and run:**
```bash
crewai install
crewai run
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Agent Configuration
- **Agents**: Defined in `src/draftycrew/config/agents.yaml`
- **Tasks**: Defined in `src/draftycrew/config/tasks.yaml`
- **Implementation**: Located in `src/draftycrew/crew.py`

### Knowledge Base
- **Best Practices**: `knowledge/openscad_best_practices.txt`
- **Common Patterns**: `knowledge/openscad_common_patterns.txt`
- **Documentation**: `knowledge/README.md`

## Usage

### Running the Crew
```bash
# From the draftycrew directory
crewai run
```

### Input
The system analyzes the image located at:
```
imagen/ejemplo_drafty.jpg
```

### Output
Generates OpenSCAD code in:
```
generated_cad_script.scad
```

## Workflow

1. **Image Analysis**: Visualizer agent analyzes the input image
2. **Technical Description**: Generates precise geometric specifications
3. **Knowledge Consultation**: CAD Generator consults knowledge base
4. **Code Generation**: Creates initial OpenSCAD code
5. **Validation**: Validates and corrects the generated code
6. **Output**: Produces final compilable OpenSCAD file

## Project Structure

```
draftycrew/
├── knowledge/                    # OpenSCAD Knowledge Base
│   ├── openscad_best_practices.txt
│   ├── openscad_common_patterns.txt
│   └── README.md
├── src/draftycrew/
│   ├── config/                   # Agent and Task configurations
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── tools/                    # Custom OpenSCAD tools
│   │   ├── openscad_knowledge_tool.py
│   │   ├── openscad_validator.py
│   │   └── __init__.py
│   ├── crew.py                   # CrewAI implementation
│   └── main.py                   # Entry point
├── generated_cad_script.scad     # Generated OpenSCAD files
├── generated_cad_script_fixed.scad
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## Troubleshooting

### Common Issues

1. **Python Version**: Ensure Python 3.12 is installed and in PATH
2. **Virtual Environment**: Verify `.venv` is activated
3. **UV Installation**: Check that UV is properly installed
4. **API Key**: Ensure `OPENAI_API_KEY` is set in environment
5. **Dependencies**: Run `pip install 'crewai[tools]'` if missing packages

### Error Messages

- **"Module not found"**: Activate virtual environment and reinstall dependencies
- **"API key not found"**: Set `OPENAI_API_KEY` in `.env` file
- **"Permission denied"**: Run PowerShell as Administrator for UV installation

## Integration with Main Project

This CrewAI project is integrated with the main Drafty system:

- **Backend**: FastAPI server that orchestrates the AI agents
- **Frontend**: React application for user interaction
- **File Exchange**: Generated OpenSCAD files are used by the web interface

## Support

- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **GitHub Repository**: [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- **Discord Community**: [discord.gg/X4JWnZnxPb](https://discord.com/invite/X4JWnZnxPb)

## License

This project is part of the DeepPunkAI Hackathon and uses the MIT License.
