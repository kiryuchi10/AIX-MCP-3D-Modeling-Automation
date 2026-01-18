"""
3D Model and ModelParameter models for storing model metadata and parameters
"""

from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, BigInteger, 
    ForeignKey, JSON, CheckConstraint
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from .base import BaseModel


class Model(BaseModel):
    """3D Model metadata and information"""
    
    __tablename__ = "models"
    
    # Basic model information
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)  # chair, car, character, architecture
    style = Column(String(100), nullable=True, index=True)     # modern, bauhaus, organic, industrial
    complexity_level = Column(Integer, CheckConstraint('complexity_level >= 1 AND complexity_level <= 10'), nullable=True)
    
    # File storage information
    file_path = Column(Text, nullable=True)
    thumbnail_path = Column(Text, nullable=True)
    file_size = Column(BigInteger, nullable=True)
    file_format = Column(String(20), nullable=True)  # blend, 3dm, fcstd, obj, fbx
    
    # Automation and generation data
    generation_script = Column(Text, nullable=True)
    mcp_command_history = Column(JSON, nullable=True)
    
    # Parametric data
    parameters = Column(JSON, nullable=True)
    constraints = Column(JSON, nullable=True)
    
    # Metadata and tagging (use JSON for SQLite compatibility)
    tags = Column(JSON, nullable=True)
    
    # AI training data
    training_prompt = Column(Text, nullable=True)
    training_difficulty = Column(Float, nullable=True)
    success_rate = Column(Float, nullable=True)
    
    # Foreign key relationships
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    creator = relationship("User", back_populates="models")
    model_parameters = relationship("ModelParameter", back_populates="model", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Model(id={self.id}, name='{self.name}', category='{self.category}')>"
    
    def to_dict(self, include_parameters=True):
        """Convert to dictionary with optional parameter inclusion"""
        data = super().to_dict()
        
        if include_parameters and self.model_parameters:
            data['detailed_parameters'] = [param.to_dict() for param in self.model_parameters]
        
        return data
    
    def get_parameter_by_name(self, parameter_name: str):
        """Get a specific parameter by name"""
        for param in self.model_parameters:
            if param.parameter_name == parameter_name:
                return param
        return None
    
    def add_tag(self, tag: str):
        """Add a tag to the model"""
        if self.tags is None:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the model"""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)
    
    def get_file_extension(self):
        """Get file extension from file_path"""
        if self.file_path:
            return self.file_path.split('.')[-1].lower()
        return None


class ModelParameter(BaseModel):
    """Detailed parameter tracking for 3D models"""
    
    __tablename__ = "model_parameters"
    
    # Parameter identification
    model_id = Column(Integer, ForeignKey("models.id", ondelete="CASCADE"), nullable=False)
    parameter_name = Column(String(100), nullable=False, index=True)
    parameter_type = Column(String(50), nullable=True)  # float, int, string, vector3, color
    
    # Parameter values (only one should be set based on parameter_type)
    value_float = Column(Float, nullable=True)
    value_int = Column(Integer, nullable=True)
    value_string = Column(Text, nullable=True)
    value_vector = Column(JSON, nullable=True)  # [x, y, z] for 3D vectors
    
    # Parameter constraints
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)
    allowed_values = Column(JSON, nullable=True)  # For enums ["oak", "pine", "mahogany"]
    
    # Parameter metadata
    description = Column(Text, nullable=True)
    unit = Column(String(20), nullable=True)  # cm, mm, degrees, etc.
    is_required = Column(Boolean, default=False, nullable=False)
    display_order = Column(Integer, nullable=True)
    
    # Relationships
    model = relationship("Model", back_populates="model_parameters")
    
    def __repr__(self):
        return f"<ModelParameter(id={self.id}, name='{self.parameter_name}', type='{self.parameter_type}')>"
    
    def get_value(self):
        """Get the parameter value based on its type"""
        if self.parameter_type == "float":
            return self.value_float
        elif self.parameter_type == "int":
            return self.value_int
        elif self.parameter_type == "string":
            return self.value_string
        elif self.parameter_type in ["vector3", "color"]:
            return self.value_vector
        return None
    
    def set_value(self, value):
        """Set the parameter value based on its type"""
        # Clear all values first
        self.value_float = None
        self.value_int = None
        self.value_string = None
        self.value_vector = None
        
        # Set the appropriate value based on type
        if self.parameter_type == "float":
            self.value_float = float(value)
        elif self.parameter_type == "int":
            self.value_int = int(value)
        elif self.parameter_type == "string":
            self.value_string = str(value)
        elif self.parameter_type in ["vector3", "color"]:
            self.value_vector = value if isinstance(value, (list, dict)) else [value]
    
    def validate_value(self, value=None):
        """Validate the parameter value against constraints"""
        if value is None:
            value = self.get_value()
        
        if value is None and self.is_required:
            return False, "Required parameter is missing"
        
        if value is None:
            return True, "Optional parameter is None"
        
        # Check min/max constraints for numeric values
        if self.parameter_type in ["float", "int"] and value is not None:
            if self.min_value is not None and value < self.min_value:
                return False, f"Value {value} is below minimum {self.min_value}"
            if self.max_value is not None and value > self.max_value:
                return False, f"Value {value} is above maximum {self.max_value}"
        
        # Check allowed values constraint
        if self.allowed_values and value not in self.allowed_values:
            return False, f"Value {value} is not in allowed values {self.allowed_values}"
        
        return True, "Valid"
    
    def to_dict(self):
        """Convert to dictionary with computed value"""
        data = super().to_dict()
        data['value'] = self.get_value()
        return data