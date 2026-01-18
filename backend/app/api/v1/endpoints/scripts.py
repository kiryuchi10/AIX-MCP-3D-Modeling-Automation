"""Script endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse, StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.script_version import ScriptVersion
from app.schemas.script import ScriptListOut, ScriptVersionOut
import io

router = APIRouter()


@router.get("/{project_id}", response_model=ScriptListOut)
def list_scripts(project_id: str, db: Session = Depends(get_db)):
    """List all script versions for a project"""
    scripts = (
        db.query(ScriptVersion)
        .filter(ScriptVersion.project_id == project_id)
        .order_by(ScriptVersion.version.desc())
        .all()
    )
    
    return ScriptListOut(
        project_id=project_id,
        versions=[
            ScriptVersionOut(
                id=s.id,
                project_id=s.project_id,
                version=s.version,
                created_at=s.created_at,
                script_length=len(s.script_text)
            )
            for s in scripts
        ]
    )


@router.get("/{project_id}/latest", response_class=PlainTextResponse)
def get_latest_script(project_id: str, db: Session = Depends(get_db)):
    """Get latest script text for a project"""
    script = (
        db.query(ScriptVersion)
        .filter(ScriptVersion.project_id == project_id)
        .order_by(ScriptVersion.version.desc())
        .first()
    )
    
    if not script:
        raise HTTPException(status_code=404, detail="No script found")
    
    return PlainTextResponse(script.script_text)


@router.get("/{script_id}/download")
def download_script(script_id: str, db: Session = Depends(get_db)):
    """Download script file"""
    script = db.query(ScriptVersion).filter(ScriptVersion.id == script_id).first()
    if not script:
        raise HTTPException(status_code=404, detail="Script not found")
    
    # Use StreamingResponse to avoid temp file
    return StreamingResponse(
        io.BytesIO(script.script_text.encode("utf-8")),
        media_type="text/x-python",
        headers={"Content-Disposition": f'attachment; filename="blender_script_v{script.version}.py"'}
    )
