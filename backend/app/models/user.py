"""
User model for authentication and user management
"""

from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    # Basic user information
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    
    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Profile information
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # API access
    api_key = Column(String(255), unique=True, nullable=True, index=True)
    api_key_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    models = relationship("Model", back_populates="creator", cascade="all, delete-orphan")
    automation_jobs = relationship("AutomationJob", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary, optionally excluding sensitive data"""
        data = super().to_dict()
        
        if not include_sensitive:
            # Remove sensitive fields from public representation
            data.pop('hashed_password', None)
            data.pop('api_key', None)
        
        return data