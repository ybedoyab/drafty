# Drafty - AI-Powered CAD Generation System

DeepPunkAI Hackathon Project

## Overview

Drafty is an intelligent system that generates CAD models from images using AI agents. The system consists of two main components:

1. **AI Agents (CrewAI)**: Two specialized agents that analyze images and generate OpenSCAD code
2. **Web Application**: React frontend with FastAPI backend for user interaction

## Project Structure

```
drafty/
├─ ai/                    # AI Logic and CrewAI Agents
│  └─ draftycrew/        # CrewAI Project (Main AI Component)
│     ├─ knowledge/      # OpenSCAD Knowledge Base
│     ├─ src/draftycrew/
│     │  ├─ config/      # Agent and Task configurations
│     │  ├─ tools/       # Custom OpenSCAD tools
│     │  ├─ crew.py      # CrewAI implementation
│     │  └─ main.py      # Entry point
│     ├─ generated_cad_script.scad      # Generated OpenSCAD files
│     └─ pyproject.toml  # CrewAI project configuration
├─ backend/              # FastAPI Backend
│  ├─ main.py
│  └─ requirements.txt
└─ frontend/             # React + Vite Frontend
   ├─ index.html
   ├─ package.json
   ├─ vite.config.js
   └─ src/
      ├─ App.jsx
      └─ main.jsx
```

## AI Agents (CrewAI) Setup

### Prerequisites

- Python 3.12
- Windows PowerShell (for UV installation)

### Installation Steps

1. **Navigate to AI directory and create virtual environment:**
```bash
cd C:\Users\Alejo\Documents\drafty\ai
py -3.12 --version
py -3.12 -m venv .venv
```

2. **Install UV package manager:**
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. **Install CrewAI:**
```bash
uv tool install crewai
```

4. **Navigate to the CrewAI project:**
```bash
cd draftycrew
```

5. **Install additional dependencies:**
```bash
pip install 'crewai[tools]'
```

6. **Install and run the crew:**
```bash
crewai install
crewai run
```

### AI Agents Configuration

The system uses two specialized AI agents:

#### **Visualizer Agent**
- **Role**: Expert CAD Design Analyzer
- **Function**: Analyzes engineering images and generates precise technical specifications
- **Tools**: VisionTool for image analysis
- **Output**: Detailed geometric descriptions with exact dimensions

#### **CAD Generator Agent**
- **Role**: Expert OpenSCAD Code Generator
- **Function**: Converts technical descriptions into functional OpenSCAD code
- **Tools**: 
  - OpenSCAD Knowledge Base Tool
  - OpenSCAD Validator Tool
- **Output**: Compilable OpenSCAD code

### Knowledge Base System

The CAD Generator agent has access to a comprehensive knowledge base:

- **Best Practices**: OpenSCAD syntax rules and guidelines
- **Common Patterns**: Templates for furniture and mechanical parts
- **Validation Tools**: Automatic error detection and correction
- **Realistic Dimensions**: Furniture-specific guidelines

### Running the AI System

```bash
# From the ai/draftycrew directory
crewai run
```

The system will:
1. Analyze the image in `imagen/ejemplo_drafty.jpg`
2. Generate technical specifications
3. Create OpenSCAD code in `generated_cad_script.scad`

## Web Application Setup

### Backend (FastAPI)

1. **Navigate to backend directory:**
```bash
cd drafty/backend
```

2. **Create virtual environment:**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the backend:**
```bash
# Option 1: Using run.py
python run.py

# Option 2: Using uvicorn directly
cd ..  # return to drafty/
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React)

1. **Navigate to frontend directory:**
```bash
cd drafty/frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run the development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Environment Variables

Create a `.env` file in `drafty/frontend` with the API URL:

```
VITE_API_URL=http://localhost:8000
```

## Production Deployment

### Build Frontend
```bash
cd drafty/frontend
npm run build  # generates dist/ directory
```

### Start Backend (serves frontend automatically)
```bash
cd drafty/backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access the application at `http://localhost:8000`

## Features

### AI-Powered CAD Generation
- **Image Analysis**: Advanced computer vision for geometric feature extraction
- **Technical Specifications**: Precise dimensional analysis and spatial relationships
- **OpenSCAD Generation**: Parametric, compilable CAD code
- **Knowledge Integration**: Best practices and validation tools

### Web Interface
- **File Upload**: Drag-and-drop image upload
- **Real-time Processing**: Live status updates
- **3D Visualization**: Interactive CAD model viewer
- **Result Download**: Export generated files

### Technical Stack
- **AI Framework**: CrewAI with GPT-4o
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TailwindCSS
- **CAD Format**: OpenSCAD with STL export

## Troubleshooting

### CrewAI Issues
- Ensure Python 3.12 is installed and in PATH
- Verify virtual environment is activated
- Check that UV is properly installed
- Ensure `OPENAI_API_KEY` is set in environment

### Backend Issues
- Verify virtual environment is activated
- Check port 8000 is available
- Ensure all dependencies are installed

### Frontend Issues
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check API URL in environment variables

## Support

- **CrewAI Documentation**: [docs.crewai.com](https://docs.crewai.com)
- **GitHub Repository**: [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- **Discord Community**: [discord.gg/X4JWnZnxPb](https://discord.com/invite/X4JWnZnxPb)

## License

This project is part of the DeepPunkAI Hackathon and uses the MIT License.
