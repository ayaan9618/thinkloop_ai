"""
Health check router
"""

from fastapi import APIRouter
from backend.app.schemas.common import HealthCheckResponse
from backend.app.config import settings

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=200,
    summary="Health Check",
    description="Check if the API is healthy and responsive",
)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthCheckResponse: Service health status
        
    Example:
        GET /health
        
        Response:
        {
            "status": "healthy",
            "version": "1.0.0-alpha",
            "environment": "production"
        }
    """
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0-alpha",
        environment=settings.environment,
    )
