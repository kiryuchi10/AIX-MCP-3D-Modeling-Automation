"""Worker tasks for background processing - Blender integration"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.config import settings
from app.models.scale_reference import ScaleReference
from app.models.extraction_result import ExtractionResult
from app.models.script_version import ScriptVersion
from app.models.job import Job
from app.models.asset import Asset
from pathlib import Path
import subprocess
import math


def run_extraction_db(job_id: str, project_id: str, params: dict):
    """Extract dimensions from scale reference - DB stored"""
    db: Session = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.id == job_id).one()
        job.status = "running"
        job.progress = 10
        db.commit()
        
        # Get scale reference
        sr = db.query(ScaleReference).filter(
            ScaleReference.project_id == project_id
        ).first()
        
        if not sr:
            job.status = "failed"
            job.message = "Scale reference not set. Please set reference dimension first."
            db.commit()
            return
        
        ref_value = float(sr.reference_value)
        
        # MVP: Generate dimensions based on ratio estimation
        # TODO: Replace with actual CV/drawing parsing (OpenCV, edge detection, OCR)
        dims = [
            {
                "name": sr.reference_name,
                "value": ref_value,
                "unit": sr.unit,
                "confidence": 0.95,
                "source": "user_reference"
            },
            {
                "name": "overall_width",
                "value": round(ref_value * 0.45, 3),
                "unit": sr.unit,
                "confidence": 0.55,
                "source": "ratio_estimation"
            },
            {
                "name": "overall_height",
                "value": round(ref_value * 0.08, 3),
                "unit": sr.unit,
                "confidence": 0.60,
                "source": "ratio_estimation"
            },
            {
                "name": "hole_diameter",
                "value": round(ref_value * 0.08, 3),
                "unit": sr.unit,
                "confidence": 0.50,
                "source": "ratio_estimation"
            },
        ]
        
        job.progress = 50
        db.commit()
        
        # Calculate next version
        latest = (
            db.query(ExtractionResult)
            .filter(ExtractionResult.project_id == project_id)
            .order_by(ExtractionResult.version.desc())
            .first()
        )
        next_ver = (latest.version + 1) if latest else 1
        
        # Save extraction result
        result = ExtractionResult(
            project_id=project_id,
            version=next_ver,
            dimensions=dims,
            features=[
                {"type": "base_plate", "shape": "rectangular"},
                {"type": "through_hole", "count": 8, "pattern": "circular"},
                {"type": "corner_fillet", "radius": ref_value * 0.02},
            ],
            tasks=[
                "Create base plate with extracted dimensions",
                "Add through holes in circular pattern",
                "Apply corner fillets",
                "Export to STL format",
            ],
        )
        db.add(result)
        db.flush()  # Ensure result.id is available
        
        job.status = "succeeded"
        job.progress = 100
        job.result = {
            "extraction_result_id": result.id,
            "version": next_ver,
            "dimensions_count": len(dims),
        }
        job.message = f"Extraction completed. Version {next_ver} created."
        db.commit()
        
    except Exception as e:
        if job:
            job.status = "failed"
            job.message = str(e)
            db.commit()
        raise
    finally:
        db.close()


def generate_script_db(job_id: str, project_id: str, params: dict):
    """Generate Blender Python script from extraction result"""
    db: Session = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.id == job_id).one()
        job.status = "running"
        job.progress = 10
        db.commit()
        
        # Get latest extraction result
        extraction = (
            db.query(ExtractionResult)
            .filter(ExtractionResult.project_id == project_id)
            .order_by(ExtractionResult.version.desc())
            .first()
        )
        
        if not extraction:
            job.status = "failed"
            job.message = "No extraction result found. Run extraction first."
            db.commit()
            return
        
        # Build dimension map
        dim_map = {d["name"]: float(d["value"]) for d in extraction.dimensions}
        
        # Extract parameters
        L = dim_map.get("overall_length_mm") or dim_map.get("overall_length") or 120.0
        W = dim_map.get("overall_width") or L * 0.45
        T = float(params.get("thickness", dim_map.get("overall_height", 5.0)))
        hole_d = dim_map.get("hole_diameter") or L * 0.08
        hole_count = int(params.get("hole_count", 8))
        ring_radius = float(params.get("hole_ring_radius", min(L, W) * 0.35))
        fillet_radius = float(params.get("fillet_radius", L * 0.02))
        
        job.progress = 40
        db.commit()
        
        # Generate script
        script_text = build_blender_script(
            L=L, W=W, T=T,
            hole_d=hole_d,
            hole_count=hole_count,
            ring_radius=ring_radius,
            fillet_radius=fillet_radius,
            project_id=project_id
        )
        
        # Calculate next version
        latest_script = (
            db.query(ScriptVersion)
            .filter(ScriptVersion.project_id == project_id)
            .order_by(ScriptVersion.version.desc())
            .first()
        )
        next_ver = (latest_script.version + 1) if latest_script else 1
        
        # Save script
        script = ScriptVersion(
            project_id=project_id,
            version=next_ver,
            script_text=script_text,
        )
        db.add(script)
        db.flush()  # Ensure script.id is available
        
        job.status = "succeeded"
        job.progress = 100
        job.result = {
            "script_id": script.id,
            "version": next_ver,
            "script_length": len(script_text),
        }
        job.message = f"Script version {next_ver} generated successfully."
        db.commit()
        
    except Exception as e:
        if job:
            job.status = "failed"
            job.message = str(e)
            db.commit()
        raise
    finally:
        db.close()


def run_blender_db(job_id: str, project_id: str, params: dict):
    """Run Blender headless - DB stored results"""
    db: Session = SessionLocal()
    job = None
    try:
        job = db.query(Job).filter(Job.id == job_id).one()
        job.status = "running"
        job.progress = 10
        db.commit()
        
        if settings.BLENDER_EXEC_MODE != "server_headless":
            job.status = "failed"
            job.message = f"Blender execution mode is '{settings.BLENDER_EXEC_MODE}', not 'server_headless'"
            db.commit()
            return
        
        # Get latest script
        script = (
            db.query(ScriptVersion)
            .filter(ScriptVersion.project_id == project_id)
            .order_by(ScriptVersion.version.desc())
            .first()
        )
        
        if not script:
            job.status = "failed"
            job.message = "No script found. Generate script first."
            db.commit()
            return
        
        # Create work directory
        workdir = Path(settings.BLENDER_WORKDIR) / project_id
        workdir.mkdir(parents=True, exist_ok=True)
        
        # Save script file
        script_path = workdir / f"script_v{script.version}.py"
        script_path.write_text(script.script_text, encoding="utf-8")
        
        job.progress = 30
        job.message = "Running Blender headless..."
        db.commit()
        
        # Run Blender
        cmd = [settings.BLENDER_PATH, "-b", "-P", str(script_path)]
        proc = subprocess.run(
            cmd,
            cwd=str(workdir),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        job.progress = 80
        db.commit()
        
        # Check output files
        output_file = workdir / f"output_{project_id}.stl"
        render_file = workdir / f"render_{project_id}.png"
        
        success = (proc.returncode == 0 and output_file.exists())
        
        if success:
            # Register result as Asset
            result_asset = Asset(
                project_id=project_id,
                asset_type="model3d",
                filename=output_file.name,
                content_type="model/stl",
                size_bytes=output_file.stat().st_size,
                storage_path=str(output_file),
            )
            db.add(result_asset)
            db.flush()  # Ensure result_asset.id is available
            
            # Register render if exists
            render_asset_id = None
            if render_file.exists():
                render_asset = Asset(
                    project_id=project_id,
                    asset_type="image",
                    filename=render_file.name,
                    content_type="image/png",
                    size_bytes=render_file.stat().st_size,
                    storage_path=str(render_file),
                )
                db.add(render_asset)
                db.flush()
                render_asset_id = render_asset.id
            
            job.status = "succeeded"
            job.progress = 100
            job.result = {
                "returncode": proc.returncode,
                "output_file": str(output_file),
                "render_file": str(render_file) if render_file.exists() else None,
                "result_asset_id": result_asset.id,
                "render_asset_id": render_asset_id,
                "stdout": proc.stdout[-2000:] if proc.stdout else None,
                "stderr": proc.stderr[-2000:] if proc.stderr else None,
            }
            job.message = "Blender execution completed successfully."
        else:
            job.status = "failed"
            job.message = f"Blender failed with return code {proc.returncode}"
            job.result = {
                "returncode": proc.returncode,
                "stdout": proc.stdout[-2000:] if proc.stdout else None,
                "stderr": proc.stderr[-2000:] if proc.stderr else None,
            }
        
        db.commit()
        
    except subprocess.TimeoutExpired:
        if job:
            job.status = "failed"
            job.message = "Blender execution timed out (>5min)"
            db.commit()
    except Exception as e:
        if job:
            job.status = "failed"
            job.message = str(e)
            db.commit()
        raise
    finally:
        db.close()


def build_blender_script(
    L: float, W: float, T: float,
    hole_d: float, hole_count: int,
    ring_radius: float, fillet_radius: float,
    project_id: str
) -> str:
    """Build Blender Python script from dimensions"""
    return f'''#!/usr/bin/env blender --python
"""
MCP 3D Automation - Generated Blender Script
Project ID: {project_id}
Generated: Automated from dimension extraction

Parameters:
- Length (L): {L} mm
- Width (W): {W} mm
- Thickness (T): {T} mm
- Hole Diameter: {hole_d} mm
- Hole Count: {hole_count}
- Ring Radius: {ring_radius} mm
- Fillet Radius: {fillet_radius} mm
"""

import bpy
import math
from mathutils import Vector

print("="*60)
print("MCP 3D Automation - Blender Script Execution")
print("="*60)

# ===== Parameters (mm -> Blender units; 1 unit = 1 mm) =====
L = {L}
W = {W}
T = {T}
hole_d = {hole_d}
hole_r = hole_d / 2.0
hole_count = {hole_count}
ring_radius = {ring_radius}
fillet_r = {fillet_radius}

print(f"Dimensions: L={{L}}, W={{W}}, T={{T}}")
print(f"Holes: {{hole_count}}x ø{{hole_d}} at R={{ring_radius}}")

# ===== Clean Scene =====
print("Cleaning scene...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Clean orphan data
for block in bpy.data.meshes:
    if block.users == 0:
        bpy.data.meshes.remove(block)

# ===== Create Base Plate =====
print("Creating base plate...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, T/2))
plate = bpy.context.active_object
plate.name = "BasePlate"
plate.scale = (L/2, W/2, T/2)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# ===== Create Hole Pattern =====
if hole_count > 0 and hole_r > 0:
    print(f"Creating {{hole_count}} holes...")
    
    # Create first hole cutter
    bpy.ops.mesh.primitive_cylinder_add(
        radius=hole_r,
        depth=T * 3,
        location=(ring_radius, 0, T/2)
    )
    cutter = bpy.context.active_object
    cutter.name = "HoleCutter_0"
    
    # Duplicate around circle
    cutters = [cutter]
    for i in range(1, hole_count):
        ang = (2 * math.pi) * (i / hole_count)
        x = math.cos(ang) * ring_radius
        y = math.sin(ang) * ring_radius
        
        dup = cutter.copy()
        dup.data = cutter.data.copy()
        dup.location = (x, y, T/2)
        dup.name = f"HoleCutter_{{i}}"
        bpy.context.collection.objects.link(dup)
        cutters.append(dup)
    
    # Join all cutters
    for obj in cutters:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = cutter
    bpy.ops.object.join()
    joined_cutter = bpy.context.active_object
    joined_cutter.name = "JoinedCutters"
    
    # Boolean difference
    print("Applying boolean difference...")
    plate.select_set(True)
    bpy.context.view_layer.objects.active = plate
    mod = plate.modifiers.new(name="HoleBoolean", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = joined_cutter
    
    bpy.ops.object.modifier_apply(modifier=mod.name)
    
    # Delete cutter
    joined_cutter.select_set(True)
    bpy.ops.object.delete(use_global=False)

# ===== Add Bevel (Fillet) =====
if fillet_r > 0:
    print(f"Adding bevel (fillet) with radius {{fillet_r}}...")
    bpy.context.view_layer.objects.active = plate
    bevel_mod = plate.modifiers.new(name="Bevel", type='BEVEL')
    bevel_mod.width = fillet_r
    bevel_mod.segments = 3
    bevel_mod.limit_method = 'ANGLE'
    bpy.ops.object.modifier_apply(modifier=bevel_mod.name)

# ===== Export STL =====
output_stl = bpy.path.abspath("//output_{project_id}.stl")
print(f"Exporting STL to: {{output_stl}}")
bpy.ops.export_mesh.stl(filepath=output_stl, use_selection=False)

# ===== Optional: Render Preview =====
print("Setting up render...")
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True

# Add camera
bpy.ops.object.camera_add(location=(L*1.5, -W*1.5, L*0.8))
camera = bpy.context.active_object
camera.rotation_euler = (math.radians(60), 0, math.radians(45))
bpy.context.scene.camera = camera

# Add light
bpy.ops.object.light_add(type='SUN', location=(L, -W, L*2))
light = bpy.context.active_object
light.data.energy = 3.0

# Render
render_path = bpy.path.abspath("//render_{project_id}.png")
print(f"Rendering preview to: {{render_path}}")
bpy.context.scene.render.filepath = render_path
bpy.ops.render.render(write_still=True)

print("="*60)
print("SUCCESS: Export and render completed")
print("="*60)
'''
