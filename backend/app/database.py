"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool

from backend.app.config import settings


def _create_engine():
    """Create a SQLAlchemy engine that works for local SQLite and MySQL."""
    url = make_url(settings.database_url)

    if url.drivername.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        if url.database in (None, "", ":memory:"):
            connect_args = {"check_same_thread": False}
        return create_engine(
            settings.database_url,
            echo=settings.database_echo,
            connect_args=connect_args,
            poolclass=NullPool if settings.environment == "testing" else QueuePool,
            pool_pre_ping=True,
        )

    return create_engine(
        settings.database_url,
        echo=settings.database_echo,
        poolclass=QueuePool if settings.environment != "testing" else NullPool,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=True,  # Verify connections before using
    )


# Create database engine
engine = _create_engine()

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    Dependency injection function for database session.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users")
        async def list_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    Should be called once at application startup if tables don't exist.
    """
    # Import models so SQLAlchemy registers all tables before create_all.
    from backend.app import models  # noqa: F401
    from backend.app.models import Base
    
    Base.metadata.create_all(bind=engine)
