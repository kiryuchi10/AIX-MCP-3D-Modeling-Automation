"""Asset schemas"""
from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


AssetType = Literal["image", "drawing2d", "model3d"]


class AssetOut(BaseModel):
    """Asset response"""
    id: str
    project_id: str
    asset_type: AssetType
    filename: str
    content_type: str
    size_bytes: int
    created_at: datetime
    updated_at: datetime
    preview_url: Optional[str] = None
    
    class Config:
        from_attributes = True
