"""Extraction endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.extraction import ScaleReferenceIn, ExtractionResultOut
from app.models.scale_reference import ScaleReference
from app.models.extraction_result import ExtractionResult

router = APIRouter()


@router.post("/scale-reference")
def set_scale_reference(payload: ScaleReferenceIn, db: Session = Depends(get_db)):
    """Set scale reference (calibration dimension) for a project"""
    # Delete existing scale reference for this project
    db.query(ScaleReference).filter(ScaleReference.project_id == payload.project_id).delete()
    
    sr = ScaleReference(
        project_id=payload.project_id,
        reference_name=payload.reference_name,
        reference_value=payload.reference_value,
        unit=payload.unit,
    )
    db.add(sr)
    db.commit()
    return {"ok": True}


@router.get("/result/{project_id}", response_model=ExtractionResultOut)
def get_extraction_result(project_id: str, db: Session = Depends(get_db)):
    """Get latest extraction result for a project"""
    result = (
        db.query(ExtractionResult)
        .filter(ExtractionResult.project_id == project_id)
        .order_by(ExtractionResult.version.desc())
        .first()
    )
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No extraction result found. Run extraction first."
        )
    
    return result
