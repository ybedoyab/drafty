
"""Connectivity test for MongoDB (Huawei Cloud DDS)."""

import os
import sys
from datetime import datetime
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

def test_mongodb_connection():
    """Test connection to MongoDB and basic operations."""
    try:
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
        
        print("🔍 Testing MongoDB connection...")
        print("=" * 50)
        
        mongodb_uri = os.getenv("DATABASE_URI")
        if not mongodb_uri:
            print("❌ Error: DATABASE_URI environment variable not set")
            print("   Set environment variables before running this script")
            return False
        
        print(f"📡 URI: {mongodb_uri}")
        print(f"🕐 Timestamp: {datetime.now().isoformat()}")
        print()
        
        print("1️⃣ Creating MongoDB client...")
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
        
        print("2️⃣ Testing ping...")
        client.admin.command('ping')
        print("✅ Ping successful!")
        
        print("3️⃣ Getting server info...")
        server_info = client.server_info()
        print(f"   MongoDB Version: {server_info.get('version', 'Unknown')}")
        
        print("4️⃣ Listing databases...")
        databases = client.list_database_names()
        print(f"   Databases: {databases}")
        
        print("5️⃣ Accessing database 'test'...")
        db = client['test']
        collections = db.list_collection_names()
        print(f"   Collections in 'test': {collections}")
        
        print("6️⃣ Inserting test document...")
        test_collection = db['test_connection']
        test_doc = {
            "test": True,
            "timestamp": datetime.utcnow(),
            "message": "Test connection successful"
        }
        result = test_collection.insert_one(test_doc)
        print(f"   Inserted ID: {result.inserted_id}")
        
        test_collection.delete_one({"_id": result.inserted_id})
        print("   Test document deleted")
        
        client.close()
        
        print()
        print("🎉 All tests passed successfully!")
        print("✅ MongoDB connection is working correctly")
        
        return True
        
    except ImportError:
        print("❌ Error: pymongo not installed")
        print("💡 Install with: pip install pymongo")
        return False
        
    except ConnectionFailure as e:
        print(f"❌ Connection error: {e}")
        print("💡 Verify:")
        print("   - Security Group port 8635 is open")
        print("   - Credentials are correct")
        print("   - VPC is properly configured")
        return False
        
    except ServerSelectionTimeoutError as e:
        print(f"❌ Timeout error: {e}")
        print("💡 Server did not respond in time")
        print("   - Check network connectivity")
        print("   - Ensure hosts are reachable")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("🚀 MongoDB Connection Test - Drafty")
    print("=" * 50)
    
    success = test_mongodb_connection()
    
    print()
    print("=" * 50)
    if success:
        print("✅ RESULT: Connection successful")
        sys.exit(0)
    else:
        print("❌ RESULT: Connection failed")
        sys.exit(1)
