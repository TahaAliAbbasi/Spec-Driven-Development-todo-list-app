"""
Application factory for the Todo List API
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize database tables."""
    # Only create tables if not in serverless environment
    # In serverless, tables should be pre-created
    if not os.getenv("VERCEL"):
        try:
            from src.database import create_db_and_tables
            create_db_and_tables()
        except Exception as e:
            print(f"Warning: Could not create database tables: {e}")
    yield


def create_app():
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Todo List API",
        description="A simple todo list API built with FastAPI and SQLModel",
        version="0.1.0",
        lifespan=lifespan
    )

    # Add CORS middleware to allow requests from frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def read_root():
        """Root endpoint for health check."""
        return {"message": "Todo List API is running!"}

    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "Todo List API"}

    # Include routes (import at the end to avoid circular imports)
    try:
        from src.api.v1.routes import tasks
        print("Routes imported successfully")
        app.include_router(tasks.router, prefix="/v1", tags=["tasks"])
        print("Routes included successfully")
    except Exception as e:
        print(f"Error importing routes: {e}")
        import traceback
        traceback.print_exc()

    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )