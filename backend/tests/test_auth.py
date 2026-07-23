import pytest
from backend.app.schemas.user import UserCreate
from backend.app.services.auth import AuthService


def test_register_user(db_session):
    """Test user registration."""
    service = AuthService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    
    user = service.register(user_data)
    assert user.email == "test@example.com"
    assert user.username == "testuser"


def test_register_duplicate_email(db_session):
    """Test duplicate email registration."""
    service = AuthService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    
    service.register(user_data)
    
    # Try registering with same email
    with pytest.raises(ValueError):
        service.register(user_data)


def test_login_user(db_session):
    """Test user login."""
    service = AuthService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    
    service.register(user_data)
    tokens = service.login("test@example.com", "password123")
    
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_login_invalid_credentials(db_session):
    """Test login with invalid credentials."""
    service = AuthService(db_session)
    
    with pytest.raises(ValueError):
        service.login("nonexistent@example.com", "password123")
