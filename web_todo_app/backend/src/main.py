from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
import sys
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    """Create and configure the FastAPI application."""
    # Add the project root to the path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Lifespan event handler to initialize database tables."""
        from src.database import create_db_and_tables
        create_db_and_tables()
        yield

    app = FastAPI(
        title="Todo List API",
        description="A simple todo list API built with FastAPI and SQLModel",
        version="0.2.0",  # Updated for chatbot feature
        lifespan=lifespan
    )

    # Add CORS middleware
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

    # Include chatbot routes (Phase III)
    try:
        from src.api.chatbot import routes as chatbot_routes
        app.include_router(chatbot_routes.router, tags=["chatbot"])
        print("Chatbot routes included successfully")
    except Exception as e:
        print(f"Error importing chatbot routes: {e}")
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