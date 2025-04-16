from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.database.connection import init_db
from app.api.v1.api import api_router

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application
    """
    # Get settings
    settings = get_settings()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        debug=settings.DEBUG
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router)
    
    # Root endpoint
    @app.get("/")
    def read_root():
        """Root endpoint."""
        return {"message": "Welcome to PasteShit API!"}
    
    # Initialize database on startup
    @app.on_event("startup")
    def startup_event():
        """Initialize database on startup."""
        init_db()
    
    return app


# Create the FastAPI app
app = create_application() 