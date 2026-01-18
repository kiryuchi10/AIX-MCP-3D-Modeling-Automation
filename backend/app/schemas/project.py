"""Project schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    """Create project request"""
    name: str = Field(..., max_length=120)
    description: Optional[str] = None


class ProjectOut(BaseModel):
    """Project response"""
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
