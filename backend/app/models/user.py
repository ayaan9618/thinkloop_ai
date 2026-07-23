"""
User model
"""

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Index, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
import uuid

from backend.app.models import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""

    STUDENT = "student"
    EDUCATOR = "educator"
    ADMIN = "admin"


class User(Base):
    """
    User account model.
    
    Attributes:
        user_id: Unique user identifier (UUID)
        email: User email address (unique)
        username: Display username
        password_hash: Bcrypt hashed password
        first_name: User's first name
        last_name: User's last name
        avatar_url: URL to user's avatar
        bio: User biography
        role: User role (student, educator, admin)
        is_verified: Email verification status
        is_active: Account status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
        last_login: Last login timestamp
    """

    __tablename__ = "user"

    user_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=True)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.STUDENT,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    sessions: Mapped[list] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    refresh_tokens: Mapped[list] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    analytics: Mapped["UserAnalytics"] = relationship(
        "UserAnalytics",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    misconceptions: Mapped[list] = relationship(
        "Misconception",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Indexes
    __table_args__ = (
        Index("idx_email", "email"),
        Index("idx_username", "username"),
        Index("idx_role", "role"),
        Index("idx_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<User(user_id={self.user_id}, email={self.email}, username={self.username})>"

    def get_full_name(self) -> str:
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def is_student(self) -> bool:
        """Check if user is a student."""
        return self.role == UserRole.STUDENT

    def is_educator(self) -> bool:
        """Check if user is an educator."""
        return self.role == UserRole.EDUCATOR

    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role == UserRole.ADMIN
