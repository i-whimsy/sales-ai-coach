"""模型配置模块 - 定义所有可用模型"""

from typing import Dict, List, Optional, Any
from enum import Enum


class ModelType(Enum):
    """模型类型"""
    LOCAL = "local"      # 本地模型
    ONLINE = "online"    # 在线模型


class TaskType(Enum):
    """任务类型"""
    ASR = "asr"              # 语音转文字
    NLP = "nlp"              # 文本分析
    SEMANTIC = "semantic"    # 语义分析


class ModelConfig:
    """模型配置类"""
    
    def __init__(
        self,
        id: str,                    # 内部唯一标识
        name: str,                  # 用户可见名称
        model_type: ModelType,       # 模型类型
        tags: List[str],             # 功能标签
        input_types: List[str],      # 输入类型
        output_types: List[str],     # 输出类型
        cost: float = 0.0,          # 成本（本地=0）
        api_key: Optional[str] = None,  # API密钥（在线模型）
        api_endpoint: Optional[str] = None,  # API端点
        priority: int = 0,           # 优先级（数字越大优先级越高）
        description: str = "",       # 描述
        model_name: str = "",        # 模型名称（用于调用）
        latency: int = 100           # 预估延迟（毫秒）
    ):
        self.id = id
        self.name = name
        self.model_type = model_type
        self.tags = tags
        self.input_types = input_types
        self.output_types = output_types
        self.cost = cost
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.priority = priority
        self.description = description
        self.model_name = model_name
        self.latency = latency
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（隐藏敏感信息）"""
        return {
            "id": self.id,
            "name": self.name,
            "model_type": self.model_type.value,
            "tags": self.tags,
            "input_types": self.input_types,
            "output_types": self.output_types,
            "cost": self.cost,
            "priority": self.priority,
            "description": self.description,
            "latency": self.latency,
            "has_api_key": bool(self.api_key)  # 不返回实际密钥
        }


# 预定义模型配置
PREDEFINED_MODELS = {
    # ========== 语音转文字 (ASR) ==========
    "whisper_base_local": ModelConfig(
        id="whisper_base_local",
        name="Whisper Base (本地)",
        model_type=ModelType.LOCAL,
        tags=["ASR", "语音转文字", "本地"],
        input_types=["audio"],
        output_types=["text"],
        cost=0.0,
        priority=100,
        description="OpenAI Whisper Base模型，本地运行，无需网络",
        model_name="base",
        latency=2000
    ),
    
    "whisper_small_local": ModelConfig(
        id="whisper_small_local",
        name="Whisper Small (本地)",
        model_type=ModelType.LOCAL,
        tags=["ASR", "语音转文字", "本地"],
        input_types=["audio"],
        output_types=["text"],
        cost=0.0,
        priority=90,
        description="OpenAI Whisper Small模型，准确率更高",
        model_name="small",
        latency=3000
    ),
    
    "whisper_api_online": ModelConfig(
        id="whisper_api_online",
        name="Whisper API (在线)",
        model_type=ModelType.ONLINE,
        tags=["ASR", "语音转文字", "在线"],
        input_types=["audio"],
        output_types=["text"],
        cost=0.006,  # 每分钟$0.006
        priority=80,
        description="OpenAI Whisper云端API，识别准确率最高",
        api_endpoint="https://api.openai.com/v1/audio/transcriptions",
        model_name="whisper-1",
        latency=500
    ),
    
    # ========== 文本分析 (NLP) ==========
    "gpt35_turbo": ModelConfig(
        id="gpt35_turbo",
        name="GPT-3.5 Turbo",
        model_type=ModelType.ONLINE,
        tags=["NLP", "文本分析", "在线"],
        input_types=["text"],
        output_types=["json", "text"],
        cost=0.002,  # 每1K tokens $0.002
        priority=70,
        description="OpenAI GPT-3.5 Turbo，速度快，成本低",
        api_endpoint="https://api.openai.com/v1/chat/completions",
        model_name="gpt-3.5-turbo",
        latency=1000
    ),
    
    "gpt4": ModelConfig(
        id="gpt4",
        name="GPT-4",
        model_type=ModelType.ONLINE,
        tags=["NLP", "文本分析", "在线"],
        input_types=["text"],
        output_types=["json", "text"],
        cost=0.03,  # 每1K tokens $0.03
        priority=60,
        description="OpenAI GPT-4，分析质量最高",
        api_endpoint="https://api.openai.com/v1/chat/completions",
        model_name="gpt-4",
        latency=2000
    ),
    
    "claude35_sonnet": ModelConfig(
        id="claude35_sonnet",
        name="Claude 3.5 Sonnet",
        model_type=ModelType.ONLINE,
        tags=["NLP", "文本分析", "在线"],
        input_types=["text"],
        output_types=["json", "text"],
        cost=0.003,  # 每1K tokens $0.003
        priority=65,
        description="Anthropic Claude 3.5 Sonnet，长文本处理能力强",
        api_endpoint="https://api.anthropic.com/v1/messages",
        model_name="claude-3-5-sonnet-20241022",
        latency=1500
    ),
    
    "deepseek_v3": ModelConfig(
        id="deepseek_v3",
        name="DeepSeek V3",
        model_type=ModelType.ONLINE,
        tags=["NLP", "文本分析", "在线"],
        input_types=["text"],
        output_types=["json", "text"],
        cost=0.001,  # 每1K tokens $0.001
        priority=75,
        description="深度求索DeepSeek V3，中文支持好，性价比高",
        api_endpoint="https://api.deepseek.com/v1/chat/completions",
        model_name="deepseek-chat",
        latency=800
    ),
    
    # ========== 语义分析 (Semantic) ==========
    "local_rule_engine": ModelConfig(
        id="local_rule_engine",
        name="本地规则引擎",
        model_type=ModelType.LOCAL,
        tags=["NLP", "语义分析", "本地"],
        input_types=["text"],
        output_types=["json"],
        cost=0.0,
        priority=50,
        description="基于关键词匹配的规则引擎，快速准确",
        model_name="rule_engine",
        latency=100
    )
}


# 场景配置 - 每个场景可用的模型
SCENE_MODELS = {
    "speech_analysis": {  # 语音分析场景
        "asr_models": ["whisper_base_local", "whisper_small_local", "whisper_api_online"],
        "nlp_models": ["local_rule_engine", "deepseek_v3", "gpt35_turbo", "claude35_sonnet", "gpt4"]
    },
    "sales_coaching": {  # 销售教练场景
        "asr_models": ["whisper_base_local", "whisper_api_online"],
        "nlp_models": ["deepseek_v3", "gpt35_turbo", "claude35_sonnet", "gpt4"]
    }
}


def get_model_config(model_id: str) -> Optional[ModelConfig]:
    """获取模型配置"""
    return PREDEFINED_MODELS.get(model_id)


def get_models_by_tag(tag: str) -> List[ModelConfig]:
    """根据标签获取模型列表"""
    return [model for model in PREDEFINED_MODELS.values() if tag in model.tags]


def get_models_by_scene(scene: str, task_type: str) -> List[ModelConfig]:
    """根据场景和任务类型获取可用模型"""
    scene_config = SCENE_MODELS.get(scene, {})
    model_ids = scene_config.get(f"{task_type}_models", [])
    
    models = []
    for model_id in model_ids:
        model = get_model_config(model_id)
        if model:
            models.append(model)
    
    return models


def get_all_models() -> List[ModelConfig]:
    """获取所有模型"""
    return list(PREDEFINED_MODELS.values())
