"""File storage utilities"""
from pathlib import Path
import shutil
import uuid
from app.core.config import settings


def get_upload_dir() -> Path:
    """Get upload directory, create if not exists"""
    upload_dir = Path(settings.LOCAL_UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def get_output_dir() -> Path:
    """Get output directory, create if not exists"""
    output_dir = Path(settings.LOCAL_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_upload_file(file_obj, filename: str) -> tuple[str, int]:
    """
    Save uploaded file and return (storage_path, size_bytes)
    
    Args:
        file_obj: File-like object
        filename: Original filename
        
    Returns:
        tuple: (storage_path as str, size_bytes as int)
    """
    upload_dir = get_upload_dir()
    asset_id = uuid.uuid4().hex
    safe_name = f"{asset_id}_{filename}"
    dest = upload_dir / safe_name
    
    with dest.open("wb") as f:
        shutil.copyfileobj(file_obj, f)
    
    size = dest.stat().st_size
    return str(dest), size
