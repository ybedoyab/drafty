"""FastAPI app: handles health, file upload, AI pipeline, and uploads CRUD."""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import shutil
import uuid
import sys
import os
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from ai.orchestrator import run_pipeline
from database import db
from storage import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Drafty Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    try:
        db.client.admin.command('ping')
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    try:
        if storage.storage_type == "huawei_obs":
            storage.s3_client.head_bucket(Bucket=storage.bucket_name)
            health_status["services"]["storage"] = f"healthy (OBS: {storage.bucket_name})"
        else:
            health_status["services"]["storage"] = f"healthy (local: {storage.upload_dir})"
    except Exception as e:
        health_status["services"]["storage"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status

@app.post("/generate")
async def generate_drawing(
    file: UploadFile = File(...),
    description: str = Form(None)
):
    """Receive image and optional description, run AI pipeline, return CAD script."""
    if file.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = f"{uuid.uuid4()}_{file.filename}"

    try:
        file_content = await file.read()
        from io import BytesIO
        file_obj = BytesIO(file_content)
        file_path = storage.save_file(file_obj, filename)
        logger.info(f"File saved: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail="Error saving file")

    try:
        record_id = db.save_upload_record(
            filename=filename,
            original_filename=file.filename,
            file_size=len(file_content),
            file_type=file.content_type,
            description=description
        )
        logger.info(f"Upload record created: {record_id}")
    except Exception as e:
        logger.error(f"Error saving upload record: {e}")

    try:
        result = run_pipeline(file_path, description)
        cad_script = result.get("cad_script", "")

        if 'record_id' in locals():
            db.update_upload_record(record_id, {
                "cad_script": cad_script,
                "status": "completed"
            })

    except Exception as e:
        logger.error(f"Error in AI pipeline: {e}")
        if 'record_id' in locals():
            db.update_upload_record(record_id, {
                "status": "failed"
            })
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "cad_script": cad_script,
        "record_id": record_id if 'record_id' in locals() else None,
        "file_url": storage.get_file_url(filename)
    }

@app.get("/uploads/{record_id}")
async def get_upload_record(record_id: str):
    """Get upload record by ID."""
    try:
        record = db.get_upload_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Upload record not found")

        if record.get("filename"):
            record["file_url"] = storage.get_file_url(record["filename"])

        return record
    except Exception as e:
        logger.error(f"Error getting upload record: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving upload record")

@app.get("/uploads")
async def list_uploads(limit: int = 50, skip: int = 0):
    """List recent uploads."""
    try:
        uploads = db.list_uploads(limit=limit, skip=skip)

        for upload in uploads:
            if upload.get("filename"):
                upload["file_url"] = storage.get_file_url(upload["filename"])

        return {
            "uploads": uploads,
            "total": len(uploads),
            "limit": limit,
            "skip": skip
        }
    except Exception as e:
        logger.error(f"Error listing uploads: {e}")
        raise HTTPException(status_code=500, detail="Error listing uploads")

@app.delete("/uploads/{record_id}")
async def delete_upload(record_id: str):
    """Delete upload record and file."""
    try:
        record = db.get_upload_record(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Upload record not found")

        if record.get("filename"):
            storage.delete_file(record["filename"])

        db.delete_upload_record(record_id)

        return {"message": "Upload deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting upload: {e}")
        raise HTTPException(status_code=500, detail="Error deleting upload") 