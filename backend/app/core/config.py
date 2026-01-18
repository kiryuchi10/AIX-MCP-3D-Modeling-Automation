"""Application configuration using Pydantic Settings"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # App
    APP_ENV: str = "dev"
    APP_NAME: str = "mcp-3d-backend"
    BASE_URL: str = "http://localhost:8000"
    CORS_ORIGINS: str = "http://localhost:5173"
    
    # Database
    DATABASE_URL: str
    
    # Redis + Queue
    REDIS_URL: str = "redis://localhost:6379/0"
    RQ_QUEUE_NAME: str = "default"
    
    # Storage
    STORAGE_MODE: str = "local"
    LOCAL_UPLOAD_DIR: str = "./uploads"
    LOCAL_OUTPUT_DIR: str = "./outputs"
    
    # Blender Integration
    BLENDER_EXEC_MODE: str = "local_only"  # local_only | server_headless
    BLENDER_PATH: str = "/usr/bin/blender"
    BLENDER_WORKDIR: str = "./outputs"
    BLENDER_UNIT_SCALE: float = 1.0
    BLENDER_EXPORT_FORMAT: str = "stl"
    
    # Security
    SECRET_KEY: str = "dev-change-me"
    
    @property
    def allowed_origins(self) -> List[str]:
        """Parse CORS origins from string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
