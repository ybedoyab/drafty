"""Database client for MongoDB (Huawei Cloud DDS)."""
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

DB_TYPE = os.getenv("DATABASE_TYPE", "mongodb")

log_level = os.getenv("BACKEND_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

if DB_TYPE == "mongodb":
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    
    class Database:
        def __init__(self):
            self.client = None
            self.db = None
            self.connect()
        
        def connect(self):
            """Connect to MongoDB."""
            try:
                mongodb_uri = os.getenv("DATABASE_URI")
                if not mongodb_uri:
                    raise ValueError("DATABASE_URI environment variable not set")
                
                self.client = MongoClient(mongodb_uri)
                db_name = os.getenv("DATABASE_NAME", "test")
                if "/" in mongodb_uri.split("?")[0]:
                    uri_parts = mongodb_uri.split("/")
                    if len(uri_parts) > 3:
                        db_name = uri_parts[-1].split("?")[0]
                
                self.db = self.client[db_name]
                
                self.client.admin.command('ping')
                logging.info(f"Connected to MongoDB successfully - Database: {db_name}")
                self._ensure_collections()
                
            except ConnectionFailure as e:
                logging.error(f"Failed to connect to MongoDB: {e}")
                raise
            except Exception as e:
                logging.error(f"Database connection error: {e}")
                raise
        
        def _ensure_collections(self):
            """Ensure required collections exist with proper indexes."""
            try:
                if "uploads" not in self.db.list_collection_names():
                    self.db.create_collection("uploads")
                    logging.info("Created 'uploads' collection")
                uploads_collection = self.db.uploads
                uploads_collection.create_index("created_at")
                uploads_collection.create_index("status")
                uploads_collection.create_index("filename")
                
                logging.info("Database collections and indexes verified")
                
            except Exception as e:
                logging.error(f"Error ensuring collections: {e}")
        
        def save_upload_record(self, filename: str, original_filename: str, 
                            file_size: int, file_type: str, 
                            cad_script: str = None, description: str = None) -> str:
            """Save upload record to database."""
            try:
                record_id = str(uuid.uuid4())
                record = {
                    "_id": record_id,
                    "filename": filename,
                    "original_filename": original_filename,
                    "file_size": file_size,
                    "file_type": file_type,
                    "cad_script": cad_script,
                    "description": description,
                    "created_at": datetime.utcnow(),
                    "status": "completed" if cad_script else "processing"
                }
                
                result = self.db.uploads.insert_one(record)
                logging.info(f"Upload record saved with ID: {record_id}")
                return record_id
                
            except Exception as e:
                logging.error(f"Error saving upload record: {e}")
                raise
        
        def get_upload_record(self, record_id: str) -> Optional[Dict[str, Any]]:
            """Get upload record by ID."""
            try:
                record = self.db.uploads.find_one({"_id": record_id})
                if record:
                    record["_id"] = str(record["_id"])
                return record
            except Exception as e:
                logging.error(f"Error getting upload record: {e}")
                return None
        
        def update_upload_record(self, record_id: str, updates: Dict[str, Any]) -> bool:
            """Update upload record."""
            try:
                result = self.db.uploads.update_one(
                    {"_id": record_id},
                    {"$set": updates}
                )
                return result.modified_count > 0
            except Exception as e:
                logging.error(f"Error updating upload record: {e}")
                return False
        
        def list_uploads(self, limit: int = 50, skip: int = 0) -> list:
            """List recent uploads."""
            try:
                cursor = self.db.uploads.find().sort("created_at", -1).skip(skip).limit(limit)
                uploads = []
                for record in cursor:
                    record["_id"] = str(record["_id"])
                    uploads.append(record)
                return uploads
            except Exception as e:
                logging.error(f"Error listing uploads: {e}")
                return []
        
        def delete_upload_record(self, record_id: str) -> bool:
            """Delete upload record from database."""
            try:
                result = self.db.uploads.delete_one({"_id": record_id})
                return result.deleted_count > 0
            except Exception as e:
                logging.error(f"Error deleting upload record: {e}")
                return False

else:
    logging.error("Only MongoDB is supported for Huawei Cloud DDS")
    raise ValueError("DB_TYPE must be 'mongodb' for Huawei Cloud deployment")

db = Database()
