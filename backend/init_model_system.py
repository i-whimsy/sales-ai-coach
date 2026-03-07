"""
Model System Initialization Script
Initialize default tags, task configs, and models
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime


def init_default_tags(db: Session):
    """Initialize default tags"""
    default_tags = [
        {"name": "语音识别", "description": "支持音频转文字功能", "color": "#ef4444"},
        {"name": "自然语言处理", "description": "支持文本分析和理解", "color": "#3b82f6"},
        {"name": "情感分析", "description": "支持情感识别和分析", "color": "#f59e0b"},
        {"name": "声纹识别", "description": "支持说话人识别", "color": "#8b5cf6"},
        {"name": "意图识别", "description": "支持用户意图识别", "color": "#10b981"},
        {"name": "评分模型", "description": "支持质量评分", "color": "#ec4899"},
        {"name": "中文", "description": "支持中文处理", "color": "#14b8a6"},
        {"name": "英文", "description": "支持英文处理", "color": "#6366f1"},
        {"name": "多语言", "description": "支持多语言处理", "color": "#f97316"},
        {"name": "高准确率", "description": "准确率较高", "color": "#22c55e"},
        {"name": "高性能", "description": "速度快，性能好", "color": "#0ea5e9"},
        {"name": "低资源", "description": "资源占用低", "color": "#84cc16"},
    ]
    
    for tag_data in default_tags:
        existing = db.query(models.ModelTag).filter(models.ModelTag.name == tag_data["name"]).first()
        if not existing:
            tag = models.ModelTag(**tag_data)
            db.add(tag)
    
    db.commit()
    print("[OK] Default tags initialized")


def init_default_task_configs(db: Session):
    """Initialize default task configs"""
    import sys
    import locale
    
    print(f"Python version: {sys.version}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    print(f"Locale: {locale.getdefaultlocale()}")
    
    default_tasks = [
        {
            "task_name": "语音转写",
            "description": "将音频文件转换为文字文本",
            "required_tags": ["语音识别"],
            "fallback_model_ids": []
        },
        {
            "task_name": "内容分析",
            "description": "分析录音内容的完整性、逻辑性",
            "required_tags": ["自然语言处理", "中文"],
            "fallback_model_ids": []
        },
        {
            "task_name": "情感识别",
            "description": "识别语音和文本中的情感倾向",
            "required_tags": ["情感分析"],
            "fallback_model_ids": []
        },
        {
            "task_name": "说话人识别",
            "description": "识别说话人身份",
            "required_tags": ["声纹识别"],
            "fallback_model_ids": []
        },
        {
            "task_name": "意图识别",
            "description": "识别客户意图和需求",
            "required_tags": ["意图识别"],
            "fallback_model_ids": []
        },
        {
            "task_name": "质量评分",
            "description": "对销售沟通质量进行综合评分",
            "required_tags": ["评分模型"],
            "fallback_model_ids": []
        },
    ]
    
    print("=== Initializing default task configurations ===")
    
    for task_data in default_tasks:
        existing = db.query(models.TaskModelConfig).filter(
            models.TaskModelConfig.task_name == task_data["task_name"]
        ).first()
        
        if not existing:
            task = models.TaskModelConfig(**task_data)
            db.add(task)
            print(f"Created: {task_data['task_name']}")
        else:
            print(f"Already exists: {existing.task_name}")
    
    db.commit()
    print("[OK] Default task configs initialized")


def init_default_models(db: Session):
    """Initialize default models"""
    # Get tag IDs
    tag_map = {}
    tags = db.query(models.ModelTag).all()
    for tag in tags:
        tag_map[tag.name] = tag.id
    
    default_models = [
        # ASR models
        {
            "name": "OpenAI Whisper API",
            "type": "online",
            "category": "ASR",
            "provider": "OpenAI",
            "api_url": "https://api.openai.com/v1/audio/transcriptions",
            "model_name": "whisper-1",
            "is_default": True,
            "config": "{\"timeout\": 60}",
            "tags": ["语音识别", "多语言", "高准确率"]
        },
        {
            "name": "字节跳动豆包ASR",
            "type": "online",
            "category": "ASR",
            "provider": "字节跳动",
            "api_url": "https://aquasearch.volces.com/v1/audio/transcriptions",
            "model_name": "speech_asr_funasr-8k-zh",
            "is_default": False,
            "config": "{\"timeout\": 60}",
            "tags": ["语音识别", "中文", "高性能"]
        },
        {
            "name": "Whisper Base (本地)",
            "type": "local",
            "category": "ASR",
            "provider": "本地",
            "model_name": "base",
            "local_path": "./models/whisper",
            "is_default": False,
            "config": "{}",
            "tags": ["语音识别", "多语言", "低资源"]
        },
        {
            "name": "Whisper Small (本地)",
            "type": "local",
            "category": "ASR",
            "provider": "本地",
            "model_name": "small",
            "local_path": "./models/whisper",
            "is_default": False,
            "config": "{}",
            "tags": ["语音识别", "多语言", "高准确率"]
        },
        {
            "name": "Whisper Medium (本地)",
            "type": "local",
            "category": "ASR",
            "provider": "本地",
            "model_name": "medium",
            "local_path": "./models/whisper",
            "is_default": False,
            "config": "{}",
            "tags": ["语音识别", "多语言", "高准确率"]
        },
        
        # NLP models
        {
            "name": "OpenAI GPT-4o",
            "type": "online",
            "category": "NLP",
            "provider": "OpenAI",
            "api_url": "https://api.openai.com/v1/chat/completions",
            "model_name": "gpt-4o",
            "is_default": True,
            "config": {"timeout": 120},
            "tags": ["自然语言处理", "中文", "高准确率"]
        },
        {
            "name": "DeepSeek V3",
            "type": "online",
            "category": "NLP",
            "provider": "深度求索",
            "api_url": "https://api.deepseek.com/v1/chat/completions",
            "model_name": "deepseek-chat",
            "is_default": False,
            "config": {"timeout": 120},
            "tags": ["自然语言处理", "中文", "高性能"]
        },
        {
            "name": "Claude 3.5 Sonnet",
            "type": "online",
            "category": "NLP",
            "provider": "Anthropic",
            "api_url": "https://api.anthropic.com/v1/messages",
            "model_name": "claude-3-5-sonnet-20240620",
            "is_default": False,
            "config": {"timeout": 120, "headers": {"anthropic-version": "2023-06-01"}},
            "tags": ["自然语言处理", "多语言", "高准确率"]
        },
    ]
    
    for model_data in default_models:
        existing = db.query(models.AIModel).filter(
            models.AIModel.name == model_data["name"]
        ).first()
        
        if not existing:
            # Extract tags
            tags = model_data.pop("tags", [])
            
            model = models.AIModel(**model_data)
            db.add(model)
            db.flush()  # Get new model ID
            
            # Add tag relations
            for tag_name in tags:
                if tag_name in tag_map:
                    relation = models.ModelTagRelation(
                        model_id=model.id,
                        tag_id=tag_map[tag_name]
                    )
                    db.add(relation)
    
    db.commit()
    
    # Update task default model IDs
    # Get default ASR and NLP models
    default_asr = db.query(models.AIModel).filter(
        models.AIModel.category == "ASR",
        models.AIModel.is_default == True
    ).first()
    
    default_nlp = db.query(models.AIModel).filter(
        models.AIModel.category == "NLP",
        models.AIModel.is_default == True
    ).first()
    
    if default_asr:
        task = db.query(models.TaskModelConfig).filter(
            models.TaskModelConfig.task_name == "语音转写"
        ).first()
        if task:
            task.default_model_id = default_asr.id
    
    if default_nlp:
        task = db.query(models.TaskModelConfig).filter(
            models.TaskModelConfig.task_name == "内容分析"
        ).first()
        if task:
            task.default_model_id = default_nlp.id
        
        task = db.query(models.TaskModelConfig).filter(
            models.TaskModelConfig.task_name == "质量评分"
        ).first()
        if task:
            task.default_model_id = default_nlp.id
    
    db.commit()
    print("[OK] Default models initialized")


def init_model_system():
    """Initialize the entire model system"""
    db = SessionLocal()
    
    try:
        # Create all tables (if not exist)
        models.Base.metadata.create_all(bind=engine)
        print("[OK] Database tables created")
        
        # Initialize default data
        init_default_tags(db)
        init_default_task_configs(db)
        init_default_models(db)
        
        print("\n=== Model System Initialization Complete ===")
        print("- 12 default tags")
        print("- 6 default task configs")
        print("- 8 default models (5 ASR, 3 NLP)")
        
    except Exception as e:
        print(f"[ERROR] Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_model_system()