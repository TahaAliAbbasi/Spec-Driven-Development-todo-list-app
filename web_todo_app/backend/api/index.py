"""
Vercel serverless function entry point
"""
import sys
import os

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import the FastAPI app
from app import app

# Vercel will use this as the ASGI application
handler = app
