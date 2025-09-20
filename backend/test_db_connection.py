#!/usr/bin/env python3
"""
Script para probar la conexión a MongoDB (Huawei Cloud DDS)

USO:
1. Configurar variables de entorno en archivo .env
2. Ejecutar: python backend/test_db_connection.py

REQUISITOS:
- Archivo .env con DATABASE_URI configurado
- PyMongo instalado: pip install pymongo
"""

import os
import sys
from datetime import datetime
from urllib.parse import quote_plus

def test_mongodb_connection():
    """Probar conexión a MongoDB"""
    try:
        # Importar pymongo
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
        
        print("🔍 Probando conexión a MongoDB...")
        print("=" * 50)
        
        # Connection string con contraseña codificada (requerido por MongoDB)
        # Usar variables de entorno para seguridad
        mongodb_uri = os.getenv("DATABASE_URI")
        if not mongodb_uri:
            print("❌ Error: DATABASE_URI environment variable not set")
            print("   Configura las variables de entorno antes de ejecutar este script")
            return False
        
        print(f"📡 URI: {mongodb_uri}")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")
        print()
        
        # Crear cliente
        print("1️⃣ Creando cliente MongoDB...")
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
        
        # Probar conexión
        print("2️⃣ Probando conexión...")
        client.admin.command('ping')
        print("✅ Conexión exitosa!")
        
        # Obtener información del servidor
        print("3️⃣ Obteniendo información del servidor...")
        server_info = client.server_info()
        print(f"   MongoDB Version: {server_info.get('version', 'Unknown')}")
        
        # Listar bases de datos
        print("4️⃣ Listando bases de datos...")
        databases = client.list_database_names()
        print(f"   Bases de datos disponibles: {databases}")
        
        # Probar acceso a la base de datos específica
        print("5️⃣ Probando acceso a base de datos 'test'...")
        db = client['test']
        collections = db.list_collection_names()
        print(f"   Colecciones en 'test': {collections}")
        
        # Probar inserción de documento de prueba
        print("6️⃣ Probando inserción de documento de prueba...")
        test_collection = db['test_connection']
        test_doc = {
            "test": True,
            "timestamp": datetime.utcnow(),
            "message": "Conexión de prueba exitosa"
        }
        result = test_collection.insert_one(test_doc)
        print(f"   Documento insertado con ID: {result.inserted_id}")
        
        # Limpiar documento de prueba
        test_collection.delete_one({"_id": result.inserted_id})
        print("   Documento de prueba eliminado")
        
        # Cerrar conexión
        client.close()
        
        print()
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("✅ La conexión a MongoDB está funcionando correctamente")
        
        return True
        
    except ImportError:
        print("❌ Error: pymongo no está instalado")
        print("💡 Instalar con: pip install pymongo")
        return False
        
    except ConnectionFailure as e:
        print(f"❌ Error de conexión: {e}")
        print("💡 Verificar:")
        print("   - Que el Security Group tenga el puerto 8635 abierto")
        print("   - Que las credenciales sean correctas")
        print("   - Que la VPC esté configurada correctamente")
        return False
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Error de timeout: {e}")
        print("💡 El servidor no responde en el tiempo esperado")
        print("   - Verificar conectividad de red")
        print("   - Verificar que los hosts sean accesibles")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 Test de Conexión MongoDB - Drafty")
    print("=" * 50)
    
    success = test_mongodb_connection()
    
    print()
    print("=" * 50)
    if success:
        print("✅ RESULTADO: Conexión exitosa")
        sys.exit(0)
    else:
        print("❌ RESULTADO: Conexión fallida")
        sys.exit(1)
