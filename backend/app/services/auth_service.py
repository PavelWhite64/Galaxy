"""
Authentication service for user management and JWT tokens.
"""
from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:
    """Service for authentication and user management."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if username or email already exists
        existing_user = self.db.query(User).filter(
            (User.username == user_data.username) | 
            (User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise ValueError("Username or email already registered")
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            display_name=user_data.display_name,
            hashed_password=hashed_password,
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        user = self.db.query(User).filter(User.username == username).first()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active or user.is_banned:
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def generate_tokens(self, user: User) -> Tuple[str, str]:
        """Generate access and refresh tokens for a user."""
        access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
        refresh_token = create_refresh_token(data={"sub": str(user.id), "username": user.username})
        return access_token, refresh_token
    
    def refresh_access_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            return None
        
        user_id = int(payload.get("sub"))
        username = payload.get("username")
        
        user = self.db.query(User).filter(User.id == user_id, User.username == username).first()
        
        if not user or not user.is_active or user.is_banned:
            return None
        
        # Generate new tokens
        new_access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
        new_refresh_token = create_refresh_token(data={"sub": str(user.id), "username": user.username})
        
        return new_access_token, new_refresh_token
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def update_user(self, user: User, update_data: UserUpdate) -> User:
        """Update user profile."""
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
