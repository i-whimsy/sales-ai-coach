"""Database models for AI Sales Coaching System"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, ForeignKey, Text
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
    report_json = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"), nullable=True)  # Selected model for analysis
    
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


class AIModel(Base):
    """AI模型配置表"""
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)  # 模型名称，如"OpenAI GPT-4o"
    # 类型: api(API模型), local_service(本地服务如Ollama), local_program(本地程序如faster-whisper)
    type = Column(String, nullable=False, default="api")
    category = Column(String, nullable=False)  # 分类: ASR/NLP/EMOTION/VOICEPRINT/INTENT/SCORE
    provider = Column(String, nullable=True)  # 提供商: OpenAI/DeepSeek/Ollama/本地等
    api_url = Column(String, nullable=True)  # API地址或服务地址
    api_key = Column(String, nullable=True)  # API密钥
    model_name = Column(String, nullable=True)  # 模型标识，如"gpt-4o", "llama3", "base"
    local_path = Column(String, nullable=True)  # 本地程序路径
    command_args = Column(String, nullable=True)  # 本地程序运行参数
    status = Column(String, default="inactive")  # 状态: active/inactive/error
    is_default = Column(Boolean, default=False)  # 是否为该分类默认模型
    config = Column(String, nullable=True)  # 其他配置参数(JSON字符串)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<AIModel(id={self.id}, name={self.name}, category={self.category}, type={self.type})>"


class ModelTag(Base):
    """模型标签表，用于标记模型能力和适用领域"""
    __tablename__ = "model_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)  # 标签名称，如"语音识别"、"中文"、"高准确率"
    description = Column(String, nullable=True)  # 标签描述
    color = Column(String, default="#3b82f6")  # 标签展示颜色
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ModelTag(id={self.id}, name={self.name})>"


class ModelTagRelation(Base):
    """模型与标签关联表"""
    __tablename__ = "model_tag_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, nullable=False, index=True)  # 关联的模型ID
    tag_id = Column(Integer, nullable=False, index=True)  # 关联的标签ID
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ModelTagRelation(model={self.model_id}, tag={self.tag_id})>"


class TaskModelConfig(Base):
    """任务与模型配置表，定义每个任务可以使用的模型"""
    __tablename__ = "task_model_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False, index=True)  # 任务名称，如"语音转写"、"内容分析"、"情感识别"
    description = Column(String, nullable=True)  # 任务描述
    required_tags = Column(JSON, nullable=True)  # 任务要求的模型标签，只有包含这些标签的模型才能被选
    default_model_id = Column(Integer, nullable=True)  # 任务默认使用的模型ID
    fallback_model_ids = Column(JSON, nullable=True)  # 备选模型ID列表，当默认模型不可用时依次尝试
    prompt_config = Column(Text, nullable=True)  # 自定义Prompt配置
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<TaskModelConfig(task={self.task_name}, default_model={self.default_model_id})>"


class ModelPreference(Base):
    """Model for storing user model preferences"""
    __tablename__ = "model_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    scene = Column(String, nullable=False, index=True)  # 场景名称
    task_type = Column(String, nullable=False, index=True)  # 任务类型
    selected_model_id = Column(Integer, nullable=True)  # 用户选择的模型ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ModelPreference(scene={self.scene}, task={self.task_type}, model={self.selected_model_id})>"
