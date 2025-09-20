import os
import logging
from typing import Optional, BinaryIO
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

# Configure logging
log_level = os.getenv("BACKEND_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

class StorageManager:
    def __init__(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "huawei_obs")
        self._setup_storage()
    
    def _setup_storage(self):
        """Setup storage based on configuration"""
        if self.storage_type == "huawei_obs":
            self._setup_huawei_obs()
        else:
            self._setup_local()
    
    def _setup_local(self):
        """Setup local file storage (fallback)"""
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        logging.info("Using local file storage")
    
    def _setup_huawei_obs(self):
        """Setup Huawei Cloud OBS storage"""
        try:
            # Validate required environment variables
            required_vars = [
                "STORAGE_OBS_ENDPOINT",
                "STORAGE_OBS_ACCESS_KEY", 
                "STORAGE_OBS_SECRET_KEY",
                "STORAGE_OBS_BUCKET_NAME"
            ]
            
            for var in required_vars:
                if not os.getenv(var):
                    raise ValueError(f"Missing required environment variable: {var}")
            
            self.s3_client = boto3.client(
                's3',
                endpoint_url=os.getenv("STORAGE_OBS_ENDPOINT"),
                aws_access_key_id=os.getenv("STORAGE_OBS_ACCESS_KEY"),
                aws_secret_access_key=os.getenv("STORAGE_OBS_SECRET_KEY"),
                region_name=os.getenv("STORAGE_OBS_REGION", "ap-southeast-1")
            )
            self.bucket_name = os.getenv("STORAGE_OBS_BUCKET_NAME")
            
            # Test bucket access
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logging.info(f"Huawei Cloud OBS storage configured - Bucket: {self.bucket_name}")
            
        except Exception as e:
            logging.error(f"Failed to setup Huawei OBS: {e}")
            logging.info("Falling back to local storage")
            self._setup_local()
            self.storage_type = "local"
    
    def save_file(self, file_content: BinaryIO, filename: str) -> str:
        """Save file and return the path/URL"""
        if self.storage_type == "local":
            return self._save_local(file_content, filename)
        else:
            return self._save_cloud(file_content, filename)
    
    def _save_local(self, file_content: BinaryIO, filename: str) -> str:
        """Save file locally"""
        file_path = self.upload_dir / filename
        with open(file_path, "wb") as f:
            f.write(file_content.read())
        return str(file_path)
    
    def _save_cloud(self, file_content: BinaryIO, filename: str) -> str:
        """Save file to cloud storage"""
        try:
            # Reset file pointer
            file_content.seek(0)
            
            # Upload to cloud storage
            self.s3_client.upload_fileobj(
                file_content,
                self.bucket_name,
                filename,
                ExtraArgs={
                    'ContentType': self._get_content_type(filename),
                    'ACL': 'public-read'  # Make files publicly accessible
                }
            )
            
            # Return public URL
            if self.storage_type == "huawei_obs":
                return f"{os.getenv('STORAGE_OBS_ENDPOINT')}/{self.bucket_name}/{filename}"
            else:
                return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
                
        except ClientError as e:
            logging.error(f"Error uploading to cloud storage: {e}")
            # Fallback to local storage
            return self._save_local(file_content, filename)
    
    def get_file_url(self, filename: str) -> str:
        """Get public URL for a file"""
        if self.storage_type == "local":
            return f"/uploads/{filename}"
        else:
            return f"{os.getenv('STORAGE_OBS_ENDPOINT')}/{self.bucket_name}/{filename}"
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file"""
        if self.storage_type == "local":
            try:
                file_path = self.upload_dir / filename
                if file_path.exists():
                    file_path.unlink()
                    return True
                return False
            except Exception as e:
                logging.error(f"Error deleting local file: {e}")
                return False
        else:
            try:
                self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
                return True
            except ClientError as e:
                logging.error(f"Error deleting cloud file: {e}")
                return False
    
    def _get_content_type(self, filename: str) -> str:
        """Get content type based on file extension"""
        ext = Path(filename).suffix.lower()
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.scad': 'text/plain',
            '.txt': 'text/plain'
        }
        return content_types.get(ext, 'application/octet-stream')

# Initialize storage manager
storage = StorageManager()
