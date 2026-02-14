"""
Vercel serverless function entry point
"""
import sys
import os

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    # Import the FastAPI app
    from app import app
    print("App imported successfully")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()

    # Create a minimal error app
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def error_root():
        return {"error": f"Failed to import main app: {str(e)}"}

    @app.get("/health")
    def error_health():
        return {"status": "error", "message": f"Import failed: {str(e)}"}

# Export for Vercel
app = app
