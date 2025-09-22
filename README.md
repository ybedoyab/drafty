# Drafty - AI OpenSCAD Code Generator 🚀
![Logo](https://github.com/user-attachments/assets/b4f00813-73d9-4598-b179-bc2755206a76)

Project for Huawei Developer Competition 2025

---

## Problem Drafty Solves

Turning ideas or sketches into functional CAD models is slow and requires technical expertise. Many users do not know OpenSCAD or advanced 3D modeling, limiting adoption of digital fabrication and part customization.

Drafty automates generation of OpenSCAD code from images, enabling anyone to obtain parametric models ready for 3D printing or manufacturing without advanced CAD knowledge.

---

## How It Works (Technical Overview)

Drafty uses a pipeline of intelligent agents (CrewAI) collaborating to analyze images and generate working OpenSCAD code:

1. Analyzer Agent
   - Analyzes the uploaded image
   - Extracts dimensions, shapes, and geometric relationships using computer vision and LLMs
   - Produces a precise structured technical description of the object

2. CAD Generator Agent
   - Consumes the technical description
   - Consults a knowledge base of OpenSCAD best practices and patterns
   - Generates parametric OpenSCAD code and automatically validates it

Result: The user receives a clean, parametric, functional OpenSCAD script, ready to visualize or modify.

---

## Tech Stack

- Frontend:
  - React + Vite
  - TailwindCSS
  - React Router DOM
- Backend:
  - FastAPI (Python)
  - AI pipeline orchestrator
- AI/Agents:
  - CrewAI (multi-agent orchestration)
  - Huawei Cloud ModelArts DeepSeek-R1-Distil-Qwen-32B
  - Custom tools: VisionTool, OpenSCAD Knowledge Tool, OpenSCAD Validator
- Other:
  - OpenSCAD (syntax and validation)
  - Recommended viewer: [ochafik.com/openscad2](https://ochafik.com/openscad2)

---

## Agent Workflow

1. The user uploads an image and optionally a description.
2. The backend runs the CrewAI pipeline:
   - The Analyzer agent produces a technical specification.
   - The CAD agent generates OpenSCAD code based on that spec and knowledge base.
   - The code is validated and auto-fixed.
3. The frontend displays the generated code, ready to copy, download, or view in [ochafik.com/openscad2](https://ochafik.com/openscad2).

---

## Getting Started

### Option 1: Docker (Recommended)

1. Clone the repo:
   ```bash
   git clone https://github.com/ybedoyab/drafty.git
   cd drafty
   ```

2. Configure environment variables:
   ```bash
   cp env.example .env
   # Fill in .env based on env.example
   ```

3. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the app:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000

### Option 2: Manual Setup

See `.env.example` for required environment variables. Create a `.env` file in the project root by copying from `.env.example` and filling your values.

#### Backend (FastAPI)

1. Go to the backend folder:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend:
   ```bash
   python run.py
   ```

#### Frontend (React)

1. Go to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the dev server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:5173 in your browser.

---

## Cloud Deployment

Drafty is optimized for deployment on Huawei Cloud with support for:

- ECS (Elastic Cloud Server): Application hosting
- DDS (Document Database Service): MongoDB
- OBS (Object Storage Service): File storage
- EIP (Elastic IP): Secure public access

For detailed deployment instructions, refer to the local deployment docs.

---

## Notes

- The generated code is plain OpenSCAD. 3D visualization is not embedded in the app, but you can view it at https://ochafik.com/openscad2 or in the OpenSCAD program.
- The frontend is optimized for a modern, clear, professional UX.
- The backend creates a unique file per uploaded image to avoid overwrites.

---

## Credits
- Project developed for Huawei Developer Competition 2025
- Repository: https://github.com/ybedoyab/drafty
- Recommended online viewer: https://ochafik.com/openscad2

---

### Authors
- Yulian Bedoya (Mechanical Engineering student)
- Marycielo Berrio Zapata (Systems Engineering student)
