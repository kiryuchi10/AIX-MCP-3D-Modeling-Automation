"""API v1 router"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, projects, assets, extraction, scripts, jobs, blender

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(extraction.router, prefix="/extraction", tags=["extraction"])
api_router.include_router(scripts.router, prefix="/scripts", tags=["scripts"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(blender.router, prefix="/blender", tags=["blender"])
