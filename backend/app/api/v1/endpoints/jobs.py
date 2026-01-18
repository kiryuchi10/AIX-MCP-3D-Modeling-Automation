"""Job endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.queue import q
from app.schemas.job import JobCreate, JobOut
from app.models.job import Job
from app.workers.tasks import run_extraction_db, generate_script_db, run_blender_db

router = APIRouter()


@router.post("", response_model=JobOut)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    """Create a new async job"""
    j = Job(
        project_id=payload.project_id,
        job_type=payload.job_type,
        status="queued",
        progress=0,
        params=payload.params or {}
    )
    db.add(j)
    db.commit()
    db.refresh(j)
    
    # Enqueue task based on job type
    if payload.job_type == "extract":
        q.enqueue(run_extraction_db, j.id, payload.project_id, j.params, job_id=j.id)
    elif payload.job_type == "generate_script":
        q.enqueue(generate_script_db, j.id, payload.project_id, j.params, job_id=j.id)
    elif payload.job_type == "run_blender":
        q.enqueue(run_blender_db, j.id, payload.project_id, j.params, job_id=j.id)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown job_type: {payload.job_type}")
    
    return j


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: str, db: Session = Depends(get_db)):
    """Get job status by ID"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("", response_model=list[JobOut])
def list_jobs(
    project_id: str = Query(None),
    status: str = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """List jobs with optional filters"""
    query = db.query(Job)
    
    if project_id:
        query = query.filter(Job.project_id == project_id)
    if status:
        query = query.filter(Job.status == status)
    
    jobs = query.order_by(Job.created_at.desc()).limit(limit).all()
    return jobs
