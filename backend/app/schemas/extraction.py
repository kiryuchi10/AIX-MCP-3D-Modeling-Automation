"""Extraction schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ScaleReferenceIn(BaseModel):
    """Set scale reference request"""
    project_id: str
    reference_name: str = Field(..., description="Reference dimension name (e.g., overall_length_mm)")
    reference_value: float = Field(..., gt=0, description="Reference value")
    unit: str = Field(default="mm", description="Unit (mm, cm, inch)")


class DimensionItem(BaseModel):
    """Dimension item"""
    name: str
    value: float
    unit: str = "mm"
    confidence: float = 0.6
    source: str = "ratio_estimation"  # ratio_estimation | mesh_bbox | user_reference


class ExtractionResultOut(BaseModel):
    """Extraction result response"""
    project_id: str
    version: int
    dimensions: List[DimensionItem]
    features: List[Dict[str, Any]] = []
    tasks: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
