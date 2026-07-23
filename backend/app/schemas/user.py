"""
User request/response schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """User registration request schema."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username (3-50 characters)",
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (minimum 8 characters)",
    )
    first_name: Optional[str] = Field(
        None,
        max_length=100,
        description="User's first name",
    )
    last_name: Optional[str] = Field(
        None,
        max_length=100,
        description="User's last name",
    )

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "username": "johndoe",
                "password": "SecurePass123!",
                "first_name": "John",
                "last_name": "Doe",
            }
        }


class UserLogin(BaseModel):
    """User login request schema."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!",
            }
        }


class UserBase(BaseModel):
    """Base user response schema."""

    user_id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    bio: Optional[str] = Field(None, description="User bio")
    role: str = Field(..., description="User role (student, educator, admin)")
    is_verified: bool = Field(..., description="Email verification status")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation time")
    updated_at: datetime = Field(..., description="Last update time")

    class Config:
        """Schema configuration."""

        from_attributes = True


class UserResponse(UserBase):
    """User response schema."""

    last_login: Optional[datetime] = Field(None, description="Last login time")


class UserUpdate(BaseModel):
    """User profile update schema."""

    first_name: Optional[str] = Field(
        None,
        max_length=100,
        description="First name",
    )
    last_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Last name",
    )
    avatar_url: Optional[str] = Field(
        None,
        max_length=500,
        description="Avatar URL",
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        description="User bio",
    )

    class Config:
        """Schema configuration."""

        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "bio": "Learning to code",
            }
        }
