"""Storage manager for Huawei OBS and local fallback."""
import os
import logging
from typing import Optional, BinaryIO
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
import requests
import hashlib
import base64
import hmac
from datetime import datetime, timezone

log_level = os.getenv("BACKEND_LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))

class StorageManager:
    def __init__(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "huawei_obs")
        self._setup_storage()
    
    def _setup_storage(self):
        """Setup storage based on configuration."""
        if self.storage_type == "huawei_obs":
            self._setup_huawei_obs()
        else:
            self._setup_local()
    
    def _setup_local(self):
        """Setup local file storage (fallback)."""
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        logging.info("Using local file storage")
    
    def _setup_huawei_obs(self):
        """Setup Huawei Cloud OBS storage."""
        try:
            logging.info("🔧 OBS Configuration Debug:")
            logging.info(f"   STORAGE_TYPE: {os.getenv('STORAGE_TYPE')}")
            logging.info(f"   STORAGE_OBS_ENDPOINT: {os.getenv('STORAGE_OBS_ENDPOINT')}")
            logging.info(f"   STORAGE_OBS_REGION: {os.getenv('STORAGE_OBS_REGION', 'ap-southeast-1')}")
            logging.info(f"   STORAGE_OBS_BUCKET_NAME: {os.getenv('STORAGE_OBS_BUCKET_NAME')}")
            
            access_key = os.getenv("STORAGE_OBS_ACCESS_KEY")
            secret_key = os.getenv("STORAGE_OBS_SECRET_KEY")
            if access_key:
                logging.info(f"   STORAGE_OBS_ACCESS_KEY: {access_key[:8]}...{access_key[-4:]}")
            else:
                logging.error("   STORAGE_OBS_ACCESS_KEY: NOT SET")
            if secret_key:
                logging.info(f"   STORAGE_OBS_SECRET_KEY: {secret_key[:8]}...{secret_key[-4:]}")
            else:
                logging.error("   STORAGE_OBS_SECRET_KEY: NOT SET")
            
            required_vars = [
                "STORAGE_OBS_ENDPOINT",
                "STORAGE_OBS_ACCESS_KEY", 
                "STORAGE_OBS_SECRET_KEY",
                "STORAGE_OBS_BUCKET_NAME"
            ]
            
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(f"Missing required environment variables: {missing_vars}")
            
            self.endpoint = os.getenv("STORAGE_OBS_ENDPOINT")
            self.region = os.getenv("STORAGE_OBS_REGION", "ap-southeast-1")
            self.bucket_name = os.getenv("STORAGE_OBS_BUCKET_NAME")
            
            regional_endpoint = f"https://obs.{self.region}.myhuaweicloud.com"
            logging.info(f"   Regional endpoint: {regional_endpoint}")
            
            self.s3_client = boto3.client(
                's3',
                endpoint_url=regional_endpoint,
                aws_access_key_id=os.getenv("STORAGE_OBS_ACCESS_KEY"),
                aws_secret_access_key=os.getenv("STORAGE_OBS_SECRET_KEY"),
                region_name=self.region,
                config=boto3.session.Config(
                    signature_version='s3v4',
                    s3={
                        'addressing_style': 'virtual'
                    }
                )
            )
            
            logging.info("✅ Huawei OBS client created successfully")
            
        except Exception as e:
            logging.error(f"❌ Error setting up Huawei OBS: {e}")
            raise
    
    def save_file(self, file_content: BinaryIO, filename: str) -> str:
        """Save file to configured storage."""
        if self.storage_type == "local":
            return self._save_local(file_content, filename)
        else:
            return self._save_cloud(file_content, filename)
    
    def _save_local(self, file_content: BinaryIO, filename: str) -> str:
        """Save file to local storage."""
        file_path = self.upload_dir / filename
        with open(file_path, "wb") as f:
            f.write(file_content.read())
        return str(file_path)
    
    def _save_cloud(self, file_content: BinaryIO, filename: str) -> str:
        """Save file to cloud storage using direct PUT method."""
        logging.info(f"☁️ Uploading file to cloud storage: {filename}")
        logging.info(f"   Bucket: {self.bucket_name}")
        logging.info(f"   Storage type: {self.storage_type}")

        try:
            file_content.seek(0)
            file_data = file_content.read()

            put_url = f"https://{self.bucket_name}.obs.ap-southeast-1.myhuaweicloud.com/{filename}"
            headers = {
                'Content-Type': self._get_content_type(filename),
                'Content-Length': str(len(file_data))
            }
            
            date_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_sign = f"PUT\n\n{headers['Content-Type']}\n{date_str}\n/{self.bucket_name}/{filename}"
            
            signature = base64.b64encode(
                hmac.new(
                    os.getenv("STORAGE_OBS_SECRET_KEY").encode('utf-8'),
                    string_to_sign.encode('utf-8'),
                    hashlib.sha1
                ).digest()
            ).decode('utf-8')
            
            headers.update({
                'Authorization': f'OBS {os.getenv("STORAGE_OBS_ACCESS_KEY")}:{signature}',
                'Date': date_str
            })
            
            put_response = requests.put(
                put_url,
                data=file_data,
                headers=headers,
                timeout=60
            )
            
            if put_response.status_code in [200, 201, 204]:
                logging.info(f"✅ File uploaded successfully via direct PUT API: {filename}")
                return self.get_public_url(filename)
            else:
                raise Exception(f"Direct PUT API failed: {put_response.status_code} - {put_response.text}")

        except Exception as e:
            logging.error(f"❌ Error uploading file to Huawei OBS via direct PUT: {e}")
            raise
    
    def get_public_url(self, filename: str) -> str:
        """Get public URL for uploaded file."""
        if self.storage_type == "huawei_obs":
            return f"https://{self.bucket_name}.obs.ap-southeast-1.myhuaweicloud.com/{filename}"
        else:
            return f"/local-files/{filename}"

    def get_file_url(self, filename: str) -> str:
        """Compatibility method used by backend/main.py to return a retrievable URL."""
        return self.get_public_url(filename)
    
    def delete_file(self, filename: str) -> bool:
        """Delete file from storage."""
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
        """Get content type based on file extension."""
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

storage = StorageManager()
