from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import uuid
import sys
from pathlib import Path

# Add the parent directory to Python path to import ai module
sys.path.append(str(Path(__file__).parent.parent))

from ai.orchestrator import run_pipeline

app = FastAPI(title="Drafty Backend", version="0.1.0")

# Allow local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Serve frontend build if present
frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

@app.post("/generate")
async def generate_drawing(
    file: UploadFile = File(...),
    description: str = Form(None)
):
    """Receive an image file and optional description, run AI pipeline, return DXF file path and CAD script."""
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = f"{uuid.uuid4()}_{file.filename}"
    image_path = UPLOAD_DIR / filename
    with image_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run the AI pipeline with optional description
    try:
        result = run_pipeline(str(image_path), description)
        dxf_path = result["dxf_file"]
        cad_script = result.get("cad_script", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "dxf_file": dxf_path,
        "cad_script": cad_script
    } 