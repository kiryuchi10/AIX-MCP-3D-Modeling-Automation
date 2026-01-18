"""
Automation Job model for tracking 3D model generation and processing jobs
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, ForeignKey, JSON, DateTime
)
from sqlalchemy.orm import relationship
from .base import BaseModel


class AutomationJob(BaseModel):
    """Automation jobs for tracking 3D model generation and processing"""
    
    __tablename__ = "automation_jobs"
    
    # Job identification and ownership
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    job_type = Column(String(50), nullable=False, index=True)  # single_generation, batch_variation, style_transfer
    status = Column(String(20), default='pending', nullable=False, index=True)  # pending, running, completed, failed
    
    # Input data
    input_prompt = Column(Text, nullable=True)
    input_parameters = Column(JSON, nullable=True)
    target_tool = Column(String(20), nullable=True)  # blender, rhino, freecad
    
    # Output data (use JSON for SQLite compatibility)
    output_model_ids = Column(JSON, nullable=True)
    output_files = Column(JSON, nullable=True)
    execution_log = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Performance metrics
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    execution_time_seconds = Column(Integer, nullable=True)
    memory_usage_mb = Column(Integer, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="automation_jobs")
    
    def __repr__(self):
        return f"<AutomationJob(id={self.id}, type='{self.job_type}', status='{self.status}')>"
    
    def start_job(self):
        """Mark job as started"""
        self.status = 'running'
        self.started_at = datetime.utcnow()
    
    def complete_job(self, output_model_ids=None, output_files=None):
        """Mark job as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        
        if output_model_ids:
            self.output_model_ids = output_model_ids
        if output_files:
            self.output_files = output_files
        
        # Calculate execution time
        if self.started_at:
            execution_time = self.completed_at - self.started_at
            self.execution_time_seconds = int(execution_time.total_seconds())
    
    def fail_job(self, error_message: str):
        """Mark job as failed"""
        self.status = 'failed'
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
        
        # Calculate execution time even for failed jobs
        if self.started_at:
            execution_time = self.completed_at - self.started_at
            self.execution_time_seconds = int(execution_time.total_seconds())
    
    def cancel_job(self):
        """Mark job as cancelled"""
        self.status = 'cancelled'
        self.completed_at = datetime.utcnow()
        
        # Calculate execution time for cancelled jobs
        if self.started_at:
            execution_time = self.completed_at - self.started_at
            self.execution_time_seconds = int(execution_time.total_seconds())
    
    def add_log_entry(self, message: str):
        """Add an entry to the execution log"""
        timestamp = datetime.utcnow().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        
        if self.execution_log:
            self.execution_log += log_entry
        else:
            self.execution_log = log_entry
    
    def get_duration(self):
        """Get job duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        elif self.started_at:
            return (datetime.utcnow() - self.started_at).total_seconds()
        return None
    
    def is_finished(self):
        """Check if job is in a finished state"""
        return self.status in ['completed', 'failed', 'cancelled']
    
    def is_running(self):
        """Check if job is currently running"""
        return self.status == 'running'
    
    def to_dict(self):
        """Convert to dictionary with computed fields"""
        data = super().to_dict()
        data['duration_seconds'] = self.get_duration()
        data['is_finished'] = self.is_finished()
        data['is_running'] = self.is_running()
        return data