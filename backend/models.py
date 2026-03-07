"""Database models for AI Sales Coaching System"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

from database import Base


class Recording(Base):
    """Model for storing recording metadata"""
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)  # Custom name given by user
    file_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    score = Column(Float, nullable=True)
    report_json = Column(JSON, nullable=True)
    transcript = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Recording(id={self.id}, name={self.name}, file_name={self.file_name}, score={self.score})>"


class ApiKeyConfig(Base):
    """Model for storing API key configurations"""
    __tablename__ = "api_key_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    openai_api_key = Column(String, nullable=True)
    deepseek_api_key = Column(String, nullable=True)
    claude_api_key = Column(String, nullable=True)
    whisper_api_key = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ApiKeyConfig(id={self.id})>"


class ScoringConfig(Base):
    """Model for storing scoring configuration"""
    __tablename__ = "scoring_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    expression_weight = Column(Float, default=0.20)
    content_weight = Column(Float, default=0.30)
    logic_weight = Column(Float, default=0.20)
    customer_weight = Column(Float, default=0.20)
    persuasion_weight = Column(Float, default=0.10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScoringConfig(id={self.id}, name={self.name})>"


class Comparison(Base):
    """Model for storing recording comparison results"""
    __tablename__ = "comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    recording1_id = Column(Integer, nullable=False)
    recording2_id = Column(Integer, nullable=False)
    comparison_result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Comparison(id={self.id}, name={self.name}, recording1={self.recording1_id}, recording2={self.recording2_id})>"


class ModelPreference(Base):
    """Model for storing user model preferences"""
    __tablename__ = "model_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    scene = Column(String, nullable=False, index=True)  # 场景名称
    task_type = Column(String, nullable=False, index=True)  # 任务类型
    selected_model_id = Column(String, nullable=True)  # 用户选择的模型ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ModelPreference(scene={self.scene}, task={self.task_type}, model={self.selected_model_id})>"
