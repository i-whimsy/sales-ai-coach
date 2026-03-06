"""Database models for AI Sales Coaching System"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

from database import Base


class Recording(Base):
    """Model for storing recording metadata"""
    __tablename__ = "recordings"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    score = Column(Float, nullable=True)
    report_json = Column(JSON, nullable=True)
    transcript = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Recording(id={self.id}, file_name={self.file_name}, score={self.score})>"


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
