"""Script schemas"""
from pydantic import BaseModel
from typing import List
from datetime import datetime


class ScriptVersionOut(BaseModel):
    """Script version info"""
    id: str
    project_id: str
    version: int
    created_at: datetime
    script_length: int
    
    class Config:
        from_attributes = True


class ScriptListOut(BaseModel):
    """Script list response"""
    project_id: str
    versions: List[ScriptVersionOut]
