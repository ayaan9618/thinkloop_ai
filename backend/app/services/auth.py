from datetime import timedelta
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.utils.security import hash_password, verify_password
from backend.app.utils.jwt import create_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def register(self, user_data: UserCreate) -> User:
        """Register new user."""
        # Check if user exists
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise ValueError("Email already registered")
        if self.db.query(User).filter(User.username == user_data.username).first():
            raise ValueError("Username already taken")
        
        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def login(self, email: str, password: str) -> dict:
        """Login user and return tokens."""
        user = self.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        access_token = create_token(
            {"sub": user.user_id},
            timedelta(hours=24)
        )
        refresh_token = create_token(
            {"sub": user.user_id},
            timedelta(days=30)
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 86400
        }
    
    def get_user_by_id(self, user_id: str) -> User:
        """Get user by ID."""
        return self.db.query(User).filter(User.user_id == user_id).first()
