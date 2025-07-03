#!/usr/bin/env python3
"""
Test script to verify backend imports and basic functionality.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all required modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test FastAPI
        import fastapi
        print("✅ FastAPI imported successfully")
        
        # Test backend main
        from backend.main import app
        print("✅ Backend main imported successfully")
        
        # Test orchestrator
        from ai.orchestrator import run_pipeline
        print("✅ Orchestrator imported successfully")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_backend_startup():
    """Test if the backend can start without errors."""
    try:
        print("\nTesting backend startup...")
        
        # This will test if the app can be created
        from backend.main import app
        print("✅ Backend app created successfully")
        
        # Test if the generate endpoint exists
        routes = [route.path for route in app.routes]
        if "/generate" in routes:
            print("✅ /generate endpoint found")
        else:
            print("❌ /generate endpoint not found")
            print(f"Available routes: {routes}")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend startup error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Drafty Backend")
    print("=" * 40)
    
    imports_ok = test_imports()
    startup_ok = test_backend_startup()
    
    print("=" * 40)
    if imports_ok and startup_ok:
        print("✅ Backend is ready to run!")
        print("\n💡 Try running: cd backend && python run.py")
    else:
        print("❌ Backend has issues. Check the errors above.") 