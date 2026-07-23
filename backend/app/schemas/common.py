"""
Common response schemas
"""

from pydantic import BaseModel, Field
from typing import Any, Optional, Generic, TypeVar


T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "error": "INVALID_INPUT",
                "message": "Email is already registered",
                "details": {"field": "email"},
            }
        }


class TokenResponse(BaseModel):
    """Authentication token response schema."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="Refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIs...",
                "refresh_token": "refresh_token_here",
                "token_type": "bearer",
                "expires_in": 86400,
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""

    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    skip: int = Field(..., description="Number of items skipped")
    limit: int = Field(..., description="Number of items returned")

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "skip": 0,
                "limit": 20,
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response schema."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment name")

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0-alpha",
                "environment": "production",
            }
        }
