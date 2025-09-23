# Drafty - AI OpenSCAD Code Generator 🚀
![Logo](https://github.com/user-attachments/assets/b4f00813-73d9-4598-b179-bc2755206a76)

**Project for Huawei Developer Competition 2025**

---

## Problem Drafty Solves

Turning ideas or sketches into functional CAD models is slow and requires technical expertise. Many users do not know OpenSCAD or advanced 3D modeling, limiting adoption of digital fabrication and part customization.

Drafty automates generation of OpenSCAD code from images, enabling anyone to obtain parametric models ready for 3D printing or manufacturing without advanced CAD knowledge.

---

## How It Works (Technical Overview)

Drafty uses a pipeline of intelligent agents (CrewAI) collaborating to analyze images and generate working OpenSCAD code:

1. **Visual Analyzer Agent**
   - Analyzes the uploaded image using computer vision
   - Extracts dimensions, shapes, and geometric relationships using LLMs
   - Produces a precise structured technical description of the object

2. **CAD Generator Agent**
   - Consumes the technical description via Huawei Cloud ModelArts
   - Consults a knowledge base of OpenSCAD best practices and patterns
   - Generates parametric OpenSCAD code and automatically validates it

**Result:** The user receives a clean, parametric, functional OpenSCAD script, ready to visualize or modify.

---

## Technology Stack

### 🎨 **Frontend Technologies**
- **React 18.2.0** - Modern UI framework with hooks
- **Vite 5.0.0** - Fast build tool and dev server
- **TailwindCSS 3.4.4** - Utility-first CSS framework
- **React Router DOM 6.23.0** - Client-side routing
- **Three.js 0.162.0** - 3D graphics library
- **@react-three/fiber 8.15.19** - React renderer for Three.js
- **@react-three/drei 9.102.6** - Useful helpers for react-three-fiber
- **Axios 1.6.0** - HTTP client for API calls
- **React Icons 4.12.0** - Icon library

### ⚙️ **Backend Technologies**
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server for FastAPI
- **Python-multipart** - File upload handling
- **Pymongo 3.11.4** - MongoDB driver (Huawei Cloud DDS)
- **Boto3 1.26.0** - AWS SDK for Huawei Cloud OBS
- **Trimesh 4.4.3** - 3D mesh processing
- **NumPy 1.24.0** - Numerical computing

### 🤖 **AI & Machine Learning**
- **CrewAI 0.193.0** - Multi-agent orchestration framework
- **LangChain OpenAI 0.2.14** - LLM integration
- **OpenAI GPT-4o** - Primary language model
- **Huawei Cloud ModelArts** - DeepSeek-R1-Distil-Qwen-32B model
- **Pillow 10.0.0** - Image processing
- **Custom Tools:**
  - VisionTool - Image analysis
  - OpenSCAD Knowledge Tool - Best practices database
  - OpenSCAD Validator - Code validation

### ☁️ **Cloud Infrastructure**
- **Huawei Cloud ECS** - Elastic Cloud Server hosting
- **Huawei Cloud DDS** - Document Database Service (MongoDB)
- **Huawei Cloud OBS** - Object Storage Service
- **Huawei Cloud EIP** - Elastic IP for public access
- **Docker & Docker Compose** - Containerization

### 🔧 **Development Tools**
- **OpenSCAD** - CAD scripting language and CLI
- **Python-dotenv** - Environment variable management
- **Pathlib2** - Enhanced path handling
- **Autoprefixer** - CSS vendor prefixing
- **PostCSS** - CSS transformation tool

---

## Agent Workflow

1. **User Input**: User uploads an image and optionally provides a description
2. **AI Pipeline Execution**: The backend runs the CrewAI pipeline:
   - **Visual Analyzer Agent** produces a technical specification using computer vision
   - **CAD Generator Agent** generates OpenSCAD code via Huawei Cloud ModelArts
   - **Validation**: The code is automatically validated and corrected
3. **Result Display**: The frontend displays the generated code with 3D visualization, ready to copy, download, or view in [ochafik.com/openscad2](https://ochafik.com/openscad2)

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

Drafty is optimized for deployment on **Huawei Cloud** with full support for:

- **ECS (Elastic Cloud Server)** - Application hosting and container orchestration
- **DDS (Document Database Service)** - MongoDB-compatible database
- **OBS (Object Storage Service)** - Scalable file storage for images and models
- **EIP (Elastic IP)** - Secure public access and load balancing

The application uses Docker containers for easy deployment and scaling across Huawei Cloud infrastructure.

---

## Key Features

- **Real-time 3D Visualization**: Built-in Three.js viewer for immediate model preview
- **Drag & Drop Interface**: Modern, intuitive file upload with example images
- **AI-Powered Analysis**: Advanced computer vision and LLM integration
- **Cloud-Native Architecture**: Scalable microservices with Huawei Cloud integration
- **OpenSCAD Compatibility**: Generates clean, parametric code ready for 3D printing
- **Professional UX**: Modern, responsive design with TailwindCSS

---

## Credits
- Project developed for Huawei Developer Competition 2025
- Repository: https://github.com/ybedoyab/drafty
- Recommended online viewer: https://ochafik.com/openscad2

---

### Authors
- Yulian Bedoya (Mechanical Engineering student)
- Marycielo Berrio Zapata (Systems Engineering student)
