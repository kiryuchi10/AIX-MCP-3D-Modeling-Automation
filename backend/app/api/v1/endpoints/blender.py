"""Blender smoke test endpoint"""
from fastapi import APIRouter, HTTPException
from pathlib import Path
import subprocess
from app.core.config import settings

router = APIRouter()


@router.post("/smoke")
def blender_smoke():
    """
    Smoke test to verify Blender integration.
    Creates a simple cube and exports STL.
    
    Returns:
        dict: Test results with status, file paths, and logs
    """
    if settings.BLENDER_EXEC_MODE != "server_headless":
        return {
            "ok": False,
            "message": f"Blender execution mode is '{settings.BLENDER_EXEC_MODE}', not 'server_headless'",
            "exec_mode": settings.BLENDER_EXEC_MODE,
            "suggestion": "Set BLENDER_EXEC_MODE=server_headless in .env to enable headless execution"
        }
    
    # Create work directory
    workdir = Path(settings.BLENDER_WORKDIR) / "smoke_test"
    workdir.mkdir(parents=True, exist_ok=True)
    
    # Create simple test script
    script_path = workdir / "smoke_test.py"
    stl_path = workdir / "smoke_cube.stl"
    
    script_content = """import bpy

# Clean scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Add cube
bpy.ops.mesh.primitive_cube_add(size=20, location=(0, 0, 10))
obj = bpy.context.active_object
obj.name = "SmokeCube"

# Export STL
export_path = bpy.path.abspath("//smoke_cube.stl")
bpy.ops.export_mesh.stl(filepath=export_path)

print("OK_EXPORT:", export_path)
"""
    
    script_path.write_text(script_content, encoding="utf-8")
    
    # Run Blender
    cmd = [settings.BLENDER_PATH, "-b", "-P", str(script_path)]
    
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(workdir),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        ok = (proc.returncode == 0 and stl_path.exists())
        
        return {
            "ok": ok,
            "returncode": proc.returncode,
            "stl_exists": stl_path.exists(),
            "stl_path": str(stl_path) if stl_path.exists() else None,
            "blender_path": settings.BLENDER_PATH,
            "workdir": str(workdir),
            "stdout_tail": proc.stdout[-500:] if proc.stdout else None,
            "stderr_tail": proc.stderr[-500:] if proc.stderr else None,
            "message": "Blender smoke test completed successfully" if ok else "Blender smoke test failed"
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=500,
            detail="Blender execution timed out (>60s). Check BLENDER_PATH configuration."
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail=f"Blender not found at {settings.BLENDER_PATH}. Please set BLENDER_PATH correctly."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Blender smoke test failed: {str(e)}"
        )
