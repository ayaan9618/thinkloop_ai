"""
SQLAlchemy models package
"""

from sqlalchemy.orm import declarative_base

# Base class for all models
Base = declarative_base()

from backend.app.models.user import User, UserRole  # noqa: E402,F401
from backend.app.models.refresh_token import RefreshToken  # noqa: E402,F401

__all__ = ["Base"]
