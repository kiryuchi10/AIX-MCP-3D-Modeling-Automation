"""Job schemas"""
from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any
from datetime import datetime


JobType = Literal["extract", "generate_script", "run_blender"]
JobStatus = Literal["queued", "running", "succeeded", "failed"]


class JobCreate(BaseModel):
    """Create job request"""
    project_id: str
    job_type: JobType
    params: Dict[str, Any] = {}


class JobOut(BaseModel):
    """Job response"""
    id: str
    project_id: str
    job_type: JobType
    status: JobStatus
    progress: int = 0
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    params: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
