#!/usr/bin/env python3
"""
Script para probar la conexión a Huawei Cloud OBS

USO:
1. Configurar variables de entorno en archivo .env
2. Ejecutar: python backend/test_obs_connection.py

REQUISITOS:
- Archivo .env con variables OBS configuradas
- boto3 instalado: pip install boto3
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

def test_obs_connection():
    """Probar conexión a Huawei Cloud OBS"""
    try:
        # Importar boto3
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        print("🔍 Probando conexión a Huawei Cloud OBS...")
        print("=" * 60)
        
        # Verificar variables de entorno
        required_vars = [
            "STORAGE_OBS_ENDPOINT",
            "STORAGE_OBS_ACCESS_KEY", 
            "STORAGE_OBS_SECRET_KEY",
            "STORAGE_OBS_BUCKET_NAME",
            "STORAGE_OBS_REGION"
        ]
        
        print("📋 Verificando variables de entorno:")
        for var in required_vars:
            value = os.getenv(var)
            if value:
                if "KEY" in var:
                    # Enmascarar claves sensibles
                    masked_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                    print(f"   ✅ {var}: {masked_value}")
                else:
                    print(f"   ✅ {var}: {value}")
            else:
                print(f"   ❌ {var}: NOT SET")
                return False
        
        print()
        
        # Crear cliente S3
        print("🚀 Creando cliente boto3 S3...")
        
        # Usar endpoint regional para Huawei OBS
        bucket_name = os.getenv("STORAGE_OBS_BUCKET_NAME")
        region = os.getenv("STORAGE_OBS_REGION", "ap-southeast-1")
        regional_endpoint = os.getenv("STORAGE_OBS_ENDPOINT", f"https://obs.{region}.myhuaweicloud.com")
        
        print(f"   Usando endpoint regional: {regional_endpoint}")
        
        # Crear sesión personalizada con configuración específica para Huawei OBS
        session = boto3.session.Session()
        
        # Configuración personalizada para compatibilidad con Huawei OBS
        config = boto3.session.Config(
            signature_version='s3v4',
            s3={
                'addressing_style': 'virtual',
                'payload_signing_enabled': False,  # Crítico: Deshabilitar firma de payload para Huawei OBS
                'use_accelerate_endpoint': False,
                'use_dualstack_endpoint': False,
                'multipart_threshold': 52428800,  # Umbral de 50MB
                'multipart_chunksize': 10485760,  # Tamaño de chunk de 10MB
                'use_ssl': True,
                'verify': True
            },
            retries={
                'max_attempts': 3,
                'mode': 'adaptive'
            },
            read_timeout=60,
            connect_timeout=60,
            # Deshabilitar cálculo automático de MD5 de contenido
            parameter_validation=False
        )
        
        # Configuración alternativa para evitar SHA256 mismatch
        # En lugar de monkey patch, usamos configuración específica
        print("   🔧 Aplicando configuración específica para Huawei OBS")
        
        s3_client = session.client(
            's3',
            endpoint_url=regional_endpoint,
            aws_access_key_id=os.getenv("STORAGE_OBS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("STORAGE_OBS_SECRET_KEY"),
            region_name=region,
            config=config
        )
        
        # Agregar event handler para remover headers SHA256
        def remove_sha256_header(event_name, **kwargs):
            if 'request' in kwargs:
                request = kwargs['request']
                if hasattr(request, 'headers') and 'x-amz-content-sha256' in request.headers:
                    del request.headers['x-amz-content-sha256']
                    print("   🔧 Removed x-amz-content-sha256 header")
        
        # Registrar el event handler
        s3_client.meta.events.register('before-sign.s3.*', remove_sha256_header)
        print("✅ Cliente S3 creado exitosamente")
        
        bucket_name = os.getenv("STORAGE_OBS_BUCKET_NAME")
        
        # Test 0: Acceso directo al bucket específico
        try:
            response = s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            print(f"❌ Error accediendo al bucket: {e}")
            return False
        
        # Test 1: Listar objetos en el bucket
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
        except ClientError as e:
            print(f"❌ Error listando objetos: {e}")
            return False
        
        # Test 2: Subir archivo de prueba
        test_filename = f"test-connection-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        test_content = f"Test file created at {datetime.now().isoformat()}"
        
        try:
            import requests
            import hmac
            import hashlib
            import base64
            from datetime import timezone
            
            # Usar PUT directo con virtual host domain
            put_url = f"https://{bucket_name}.obs.ap-southeast-1.myhuaweicloud.com/{test_filename}"
            headers = {
                'Content-Type': 'text/plain',
                'Content-Length': str(len(test_content.encode('utf-8')))
            }
            
            # Crear signature para PUT directo
            date_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_sign = f"PUT\n\n{headers['Content-Type']}\n{date_str}\n/{bucket_name}/{test_filename}"
            
            # Crear signature
            signature = base64.b64encode(
                hmac.new(
                    os.getenv("STORAGE_OBS_SECRET_KEY").encode('utf-8'),
                    string_to_sign.encode('utf-8'),
                    hashlib.sha1
                ).digest()
            ).decode('utf-8')
            
            # Agregar headers de autenticación
            headers.update({
                'Authorization': f'OBS {os.getenv("STORAGE_OBS_ACCESS_KEY")}:{signature}',
                'Date': date_str
            })
            
            # Hacer PUT directo
            put_response = requests.put(
                put_url,
                data=test_content.encode('utf-8'),
                headers=headers,
                timeout=60
            )
            
            if put_response.status_code not in [200, 201, 204]:
                print(f"❌ Subida falló: {put_response.status_code} - {put_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en subida: {e}")
            return False
        
        # Test 3: Descargar archivo de prueba
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=test_filename)
        except ClientError as e:
            print(f"❌ Error descargando archivo: {e}")
            return False
        
        # Test 4: Generar URL pública
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': test_filename},
                ExpiresIn=3600
            )
        except ClientError as e:
            print(f"❌ Error generando URL: {e}")
            return False
        
        # Test 5: Probar subida de imagen
        try:
            import base64
            
            # Crear una imagen simple en formato PNG (1x1 pixel transparente)
            png_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
            image_filename = f"test-image-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
            
            # Usar PUT directo para imagen
            put_url = f"https://{bucket_name}.obs.ap-southeast-1.myhuaweicloud.com/{image_filename}"
            headers = {
                'Content-Type': 'image/png',
                'Content-Length': str(len(png_data))
            }
            
            # Crear signature para PUT directo
            date_str = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
            string_to_sign = f"PUT\n\n{headers['Content-Type']}\n{date_str}\n/{bucket_name}/{image_filename}"
            
            # Crear signature
            signature = base64.b64encode(
                hmac.new(
                    os.getenv("STORAGE_OBS_SECRET_KEY").encode('utf-8'),
                    string_to_sign.encode('utf-8'),
                    hashlib.sha1
                ).digest()
            ).decode('utf-8')
            
            # Agregar headers de autenticación
            headers.update({
                'Authorization': f'OBS {os.getenv("STORAGE_OBS_ACCESS_KEY")}:{signature}',
                'Date': date_str
            })
            
            # Hacer PUT directo
            put_response = requests.put(
                put_url,
                data=png_data,
                headers=headers,
                timeout=60
            )
            
            if put_response.status_code not in [200, 201, 204]:
                print(f"❌ Subida de imagen falló: {put_response.status_code} - {put_response.text}")
                return False
            
            # Limpiar imagen de prueba
            s3_client.delete_object(Bucket=bucket_name, Key=image_filename)
            
        except Exception as e:
            print(f"❌ Error con imagen: {e}")
            return False
        
        # Test 6: Eliminar archivo de prueba
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=test_filename)
        except ClientError as e:
            print(f"❌ Error eliminando archivo: {e}")
            return False
        
        return True
        
    except ImportError:
        print("❌ Error: boto3 no está instalado")
        print("💡 Instalar con: pip install boto3")
        return False
        
    except NoCredentialsError:
        print("❌ Error: Credenciales no encontradas")
        print("💡 Verificar que las variables de entorno estén configuradas correctamente")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Test de Conexión Huawei Cloud OBS - Drafty")
    print("=" * 60)
    
    success = test_obs_connection()
    
    print()
    print("=" * 60)
    if success:
        print("✅ RESULTADO: Conexión OBS exitosa")
        sys.exit(0)
    else:
        print("❌ RESULTADO: Conexión OBS fallida")
        sys.exit(1)
