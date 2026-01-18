"""Asset endpoints"""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.storage import save_upload_file
from app.models.asset import Asset
from app.schemas.asset import AssetOut

router = APIRouter()


@router.post("/upload", response_model=list[AssetOut])
def upload_assets(
    project_id: str = Form(...),
    asset_type: str = Form(...),
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """Upload assets (images, drawings, 3D models)"""
    outs = []
    for uf in files:
        path, size = save_upload_file(uf.file, uf.filename)
        a = Asset(
            project_id=project_id,
            asset_type=asset_type,
            filename=uf.filename,
            content_type=uf.content_type or "application/octet-stream",
            size_bytes=size,
            storage_path=path,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        outs.append(a)
    return outs


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    """Get asset by ID"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.get("/{asset_id}/download")
def download_asset(asset_id: str, db: Session = Depends(get_db)):
    """Download asset file"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return FileResponse(asset.storage_path, filename=asset.filename)


@router.get("/{asset_id}/preview")
def preview_asset(asset_id: str, db: Session = Depends(get_db)):
    """Preview asset (for images/renders)"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return FileResponse(asset.storage_path, filename=asset.filename)
