#!/usr/bin/env python3
"""Connectivity test for Huawei Cloud OBS using boto3 and direct PUT."""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def test_obs_connection():
    """Test Huawei Cloud OBS connectivity and basic operations."""
    try:
        # Importar boto3
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        print("🔍 Testing Huawei Cloud OBS connectivity...")
        print("=" * 60)
        
        required_vars = [
            "STORAGE_OBS_ENDPOINT",
            "STORAGE_OBS_ACCESS_KEY", 
            "STORAGE_OBS_SECRET_KEY",
            "STORAGE_OBS_BUCKET_NAME",
            "STORAGE_OBS_REGION"
        ]
        
        print("📋 Checking environment variables:")
        for var in required_vars:
            value = os.getenv(var)
            if value:
                if "KEY" in var:
                    masked_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                    print(f"   ✅ {var}: {masked_value}")
                else:
                    print(f"   ✅ {var}: {value}")
            else:
                print(f"   ❌ {var}: NOT SET")
                return False
        
        print()
        
        print("🚀 Creating boto3 S3 client...")
        
        bucket_name = os.getenv("STORAGE_OBS_BUCKET_NAME")
        region = os.getenv("STORAGE_OBS_REGION", "ap-southeast-1")
        regional_endpoint = os.getenv("STORAGE_OBS_ENDPOINT", f"https://obs.{region}.myhuaweicloud.com")
        
        print(f"   Using regional endpoint: {regional_endpoint}")
        
        session = boto3.session.Session()
        
        config = boto3.session.Config(
            signature_version='s3v4',
            s3={
                'addressing_style': 'virtual',
                'payload_signing_enabled': False,
                'use_accelerate_endpoint': False,
                'use_dualstack_endpoint': False,
                'multipart_threshold': 52428800,
                'multipart_chunksize': 10485760,
                'use_ssl': True,
                'verify': True
            },
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            },
            read_timeout=60,
            connect_timeout=60,
            parameter_validation=False
        )
        
        print("   🔧 Applying Huawei OBS specific configuration")
        
        s3_client = session.client(
            's3',
            endpoint_url=regional_endpoint,
            aws_access_key_id=os.getenv("STORAGE_OBS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("STORAGE_OBS_SECRET_KEY"),
            region_name=region,
            config=config
        )
        
        def remove_sha256_header(event_name, **kwargs):
            if 'request' in kwargs:
                request = kwargs['request']
                if hasattr(request, 'headers') and 'x-amz-content-sha256' in request.headers:
                    del request.headers['x-amz-content-sha256']
                    print("   🔧 Removed x-amz-content-sha256 header")
        
        s3_client.meta.events.register('before-sign.s3.*', remove_sha256_header)
        print("✅ S3 client created successfully")
        
        bucket_name = os.getenv("STORAGE_OBS_BUCKET_NAME")
        
        try:
            response = s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            print(f"❌ Error accessing bucket: {e}")
            return False
        
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
        except ClientError as e:
            print(f"❌ Error listing objects: {e}")
            return False
        
        test_filename = f"test-connection-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        test_content = f"Test file created at {datetime.now().isoformat()}"
        
        try:
            import requests
            import hmac
            import hashlib
            import base64
            from datetime import timezone
            
            put_url = f"https://{bucket_name}.obs.ap-southeast-1.myhuaweicloud.com/{test_filename}"
            headers = {
                'Content-Type': 'text/plain',
                'Content-Length': str(len(test_content.encode('utf-8')))
            }
            
            date_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_sign = f"PUT\n\n{headers['Content-Type']}\n{date_str}\n/{bucket_name}/{test_filename}"
            
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
                data=test_content.encode('utf-8'),
                headers=headers,
                timeout=60
            )
            
            if put_response.status_code not in [200, 201, 204]:
                print(f"❌ Upload failed: {put_response.status_code} - {put_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
        
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=test_filename)
        except ClientError as e:
            print(f"❌ Download error: {e}")
            return False
        
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': test_filename},
                ExpiresIn=3600
            )
        except ClientError as e:
            print(f"❌ Error generating URL: {e}")
            return False
        
        try:
            import base64
            
            png_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
            image_filename = f"test-image-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
            
            put_url = f"https://{bucket_name}.obs.ap-southeast-1.myhuaweicloud.com/{image_filename}"
            headers = {
                'Content-Type': 'image/png',
                'Content-Length': str(len(png_data))
            }
            
            date_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_sign = f"PUT\n\n{headers['Content-Type']}\n{date_str}\n/{bucket_name}/{image_filename}"
            
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
                data=png_data,
                headers=headers,
                timeout=60
            )
            
            if put_response.status_code not in [200, 201, 204]:
                print(f"❌ Image upload failed: {put_response.status_code} - {put_response.text}")
                return False
            
            s3_client.delete_object(Bucket=bucket_name, Key=image_filename)
            
        except Exception as e:
            print(f"❌ Image error: {e}")
            return False
        
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=test_filename)
        except ClientError as e:
            print(f"❌ Deletion error: {e}")
            return False
        
        return True
        
    except ImportError:
        print("❌ Error: boto3 not installed")
        print("💡 Install with: pip install boto3")
        return False
        
    except NoCredentialsError:
        print("❌ Error: Credentials not found")
        print("💡 Verify that environment variables are set correctly")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Huawei Cloud OBS Connection Test - Drafty")
    print("=" * 60)
    
    success = test_obs_connection()
    
    print()
    print("=" * 60)
    if success:
        print("✅ RESULT: OBS connection successful")
        sys.exit(0)
    else:
        print("❌ RESULT: OBS connection failed")
        sys.exit(1)
