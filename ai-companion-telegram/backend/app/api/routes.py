"""
FastAPI routes for health checks and basic API endpoints.
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["health"])


class HealthResponse(BaseModel):
    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns the service status.
    """
    return HealthResponse(
        status="healthy",
        message="AI Companion backend is running"
    )


@router.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "AI Companion API",
        "version": "1.0.0",
        "description": "Personal AI Companion & Assistant (Telegram Bot + Local LLM)"
    }
