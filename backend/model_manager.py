"""模型管理器 - 统一管理模型选择、调用和配置"""

from typing import Dict, List, Optional, Any, Callable
from models_config import (
    ModelConfig,
    ModelType,
    get_model_config,
    get_models_by_tag,
    get_models_by_scene,
    get_all_models,
    PREDEFINED_MODELS
)
import whisper
import openai
from anthropic import Anthropic
import json


class ModelManager:
    """模型管理器类"""
    
    def __init__(self, api_config: Optional[Dict[str, str]] = None):
        """初始化模型管理器
        
        Args:
            api_config: API密钥配置，格式如 {"openai_api_key": "sk-xxx"}
        """
        self.api_config = api_config or {}
        self._clients = {}
        self._whisper_models = {}
    
    def get_available_models(
        self,
        scene: Optional[str] = None,
        task_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "priority",
        prefer_local: bool = True
    ) -> List[ModelConfig]:
        """获取可用模型列表
        
        Args:
            scene: 场景名称
            task_type: 任务类型
            tags: 标签列表
            sort_by: 排序方式 (priority | cost | latency)
            prefer_local: 是否优先本地模型
        
        Returns:
            模型配置列表
        """
        # 获取候选模型
        if scene and task_type:
            models = get_models_by_scene(scene, task_type)
        elif tags:
            models = []
            for tag in tags:
                models.extend(get_models_by_tag(tag))
            # 去重
            seen = set()
            unique_models = []
            for model in models:
                if model.id not in seen:
                    seen.add(model.id)
                    unique_models.append(model)
            models = unique_models
        else:
            models = get_all_models()
        
        # 按优先级排序（优先本地，然后按指定条件）
        def sort_key(model: ModelConfig) -> tuple:
            # 本地模型优先
            local_priority = 0 if model.model_type == ModelType.LOCAL else 1
            if sort_by == "priority":
                return (local_priority, -model.priority)
            elif sort_by == "cost":
                return (local_priority, model.cost)
            elif sort_by == "latency":
                return (local_priority, model.latency)
            else:
                return (local_priority, -model.priority)
        
        models.sort(key=sort_key)
        return models
    
    def select_best_model(
        self,
        scene: str,
        task_type: str,
        tags: Optional[List[str]] = None,
        prefer_local: bool = True
    ) -> Optional[ModelConfig]:
        """选择最优模型
        
        Args:
            scene: 场景名称
            task_type: 任务类型
            tags: 标签列表
            prefer_local: 是否优先本地模型
        
        Returns:
            最优模型配置
        """
        models = self.get_available_models(
            scene=scene,
            task_type=task_type,
            tags=tags,
            prefer_local=prefer_local
        )
        
        if not models:
            return None
        
        # 检查模型是否可用（在线模型需要API密钥）
        for model in models:
            if self._is_model_available(model):
                return model
        
        return None
    
    def _is_model_available(self, model: ModelConfig) -> bool:
        """检查模型是否可用"""
        if model.model_type == ModelType.LOCAL:
            return True
        
        # 在线模型检查API密钥
        if model.api_endpoint and "openai" in model.api_endpoint:
            return bool(self.api_config.get("openai_api_key"))
        elif model.api_endpoint and "anthropic" in model.api_endpoint:
            return bool(self.api_config.get("claude_api_key"))
        elif model.api_endpoint and "deepseek" in model.api_endpoint:
            return bool(self.api_config.get("deepseek_api_key"))
        
        return False
    
    def get_client(self, model: ModelConfig):
        """获取模型客户端（缓存）"""
        if model.id in self._clients:
            return self._clients[model.id]
        
        client = None
        
        if model.model_type == ModelType.LOCAL:
            if "whisper" in model.id:
                # Whisper模型延迟加载
                pass
            client = None
        
        elif model.model_type == ModelType.ONLINE:
            if "openai" in model.api_endpoint:
                api_key = self.api_config.get("openai_api_key")
                if api_key:
                    client = openai.OpenAI(api_key=api_key)
            elif "anthropic" in model.api_endpoint:
                api_key = self.api_config.get("claude_api_key")
                if api_key:
                    client = Anthropic(api_key=api_key)
            elif "deepseek" in model.api_endpoint:
                api_key = self.api_config.get("deepseek_api_key")
                if api_key:
                    client = openai.OpenAI(
                        api_key=api_key,
                        base_url="https://api.deepseek.com/v1"
                    )
        
        if client:
            self._clients[model.id] = client
        
        return client
    
    def get_whisper_model(self, model_config: ModelConfig):
        """获取Whisper模型（缓存）"""
        if model_config.id in self._whisper_models:
            return self._whisper_models[model_config.id]
        
        if "whisper" in model_config.id:
            model = whisper.load_model(model_config.model_name)
            self._whisper_models[model_config.id] = model
            return model
        
        return None
    
    def get_models_for_ui(
        self,
        scene: str,
        task_type: str
    ) -> List[Dict[str, Any]]:
        """获取用于UI展示的模型列表"""
        models = self.get_available_models(scene=scene, task_type=task_type)
        
        ui_models = []
        for model in models:
            ui_model = model.to_dict()
            # 添加标签显示文本（如 "语音转文字 - Whisper Base (本地)"）
            display_name = model.name
            if model.tags:
                main_tag = model.tags[0]
                display_name = f"{main_tag} - {model.name}"
            
            ui_model["display_name"] = display_name
            ui_model["available"] = self._is_model_available(model)
            ui_models.append(ui_model)
        
        return ui_models
    
    def set_api_key(self, provider: str, api_key: str):
        """设置API密钥"""
        self.api_config[provider] = api_key
        # 清除相关客户端缓存
        keys_to_remove = []
        for model_id, client in self._clients.items():
            if provider in model_id:
                keys_to_remove.append(model_id)
        for key in keys_to_remove:
            del self._clients[key]


# 单例模式
_instance: Optional[ModelManager] = None


def get_model_manager(api_config: Optional[Dict[str, str]] = None) -> ModelManager:
    """获取模型管理器单例"""
    global _instance
    if _instance is None:
        _instance = ModelManager(api_config)
    elif api_config:
        _instance.api_config.update(api_config)
    return _instance
