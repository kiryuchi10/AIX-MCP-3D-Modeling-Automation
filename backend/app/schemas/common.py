"""Common schemas"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class APIResponse(BaseModel):
    """Standard API response"""
    ok: bool = True
    message: Optional[str] = None


class Timestamped(BaseModel):
    """Base model with timestamps"""
    created_at: datetime
    updated_at: datetime
