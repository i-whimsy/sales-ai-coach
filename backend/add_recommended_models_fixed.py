import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# 定义所有模型类别
categories = [
    ("ASR", "语音识别"),
    ("NLP", "自然语言处理"), 
    ("EMOTION", "情感分析"),
    ("VOICEPRINT", "声纹识别"),
    ("INTENT", "意图识别"),
    ("SCORE", "评分模型")
]

# 为每个类别添加建议模型
models_to_add = []

# ASR 类别
models_to_add.append({
    "name": "OpenAI Whisper API",
    "type": "api",
    "category": "ASR",
    "provider": "OpenAI",
    "api_url": "https://api.openai.com/v1/audio/transcriptions",
    "api_key": "sk-xxx",  # 用户需要自己填写
    "model_name": "whisper-1",
    "description": "OpenAI官方语音识别API，支持多语言，高准确率",
    "is_default": True,
    "status": "active",
    "config": json.dumps({"timeout": 60})
})

models_to_add.append({
    "name": "本地 Whisper (faster-whisper)",
    "type": "local_program",
    "category": "ASR",
    "provider": "本地",
    "command_path": "python",
    "command_args": "-m faster_whisper --model small --language zh",
    "description": "本地faster-whisper模型，无需API，支持中文",
    "is_default": True,  # 本地模型设为默认
    "status": "active",
    "config": json.dumps({"device": "cpu", "compute_type": "int8"})
})

# NLP 类别
models_to_add.append({
    "name": "OpenAI GPT-4o",
    "type": "api",
    "category": "NLP",
    "provider": "OpenAI",
    "api_url": "https://api.openai.com/v1/chat/completions",
    "api_key": "sk-xxx",  # 用户需要自己填写
    "model_name": "gpt-4o",
    "description": "OpenAI最新多模态模型，强大的自然语言理解能力",
    "is_default": True,
    "status": "active",
    "config": json.dumps({"temperature": 0.7, "max_tokens": 2000})
})

models_to_add.append({
    "name": "本地 Ollama Llama3",
    "type": "local_service",
    "category": "NLP",
    "provider": "Ollama",
    "api_url": "http://localhost:11434/api/generate",  # 使用api_url字段作为服务地址
    "model_name": "llama3:8b",
    "description": "本地Ollama运行的Llama3模型，支持中文",
    "is_default": True,  # 本地模型设为默认
    "status": "active",
    "config": json.dumps({"temperature": 0.7, "stream": False})
})

# EMOTION 类别
models_to_add.append({
    "name": "百度情感分析API",
    "type": "api",
    "category": "EMOTION",
    "provider": "百度",
    "api_url": "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify",
    "api_key": "xxx",  # 用户需要自己填写
    "description": "百度AI情感分析API，支持中文文本情感识别",
    "is_default": True,
    "status": "active",
    "config": json.dumps({"charset": "UTF-8"})
})

models_to_add.append({
    "name": "本地情感分析模型",
    "type": "local_program",
    "category": "EMOTION",
    "provider": "本地",
    "command_path": "python",
    "command_args": "-m transformers_pipeline --task sentiment-analysis --model uer/roberta-base-finetuned-chinanews-chinese",
    "description": "基于RoBERTa的中文情感分析模型",
    "is_default": True,  # 本地模型设为默认
    "status": "active",
    "config": json.dumps({"batch_size": 16})
})

# VOICEPRINT 类别
models_to_add.append({
    "name": "讯飞声纹识别API",
    "type": "api",
    "category": "VOICEPRINT",
    "provider": "讯飞",
    "api_url": "https://api.xfyun.cn/v1/service/v1/iat",
    "api_key": "xxx",  # 用户需要自己填写
    "description": "讯飞声纹识别API，支持说话人识别",
    "is_default": True,
    "status": "active",
    "config": json.dumps({"language": "zh_cn"})
})

models_to_add.append({
    "name": "本地声纹识别",
    "type": "local_program",
    "category": "VOICEPRINT",
    "provider": "本地",
    "command_path": "python",
    "command_args": "-m speechbrain spkrec-ecapa-voxceleb",
    "description": "基于SpeechBrain的声纹识别模型",
    "is_default": True,  # 本地模型设为默认
    "status": "active",
    "config": json.dumps({"device": "cpu"})
})

# INTENT 类别
models_to_add.append({
    "name": "阿里云意图识别",
    "type": "api",
    "category": "INTENT",
    "provider": "阿里云",
    "api_url": "https://nlp.cn-shanghai.aliyuncs.com/v2/intent",
    "api_key": "xxx",  # 用户需要自己填写
    "description": "阿里云自然语言处理API，支持意图识别",
    "is_default": True,
    "status": "active",
    "config": json.dumps({"domain": "general"})
})

models_to_add.append({
    "name": "本地意图识别模型",
    "type": "local_program",
    "category": "INTENT",
    "provider": "本地",
    "command_path": "python",
    "command_args": "-m paddlenlp_cli --task text_classification --model ernie-3.0-base-zh",
    "description": "基于ERNIE的中文意图识别模型",
    "is_default": True,  # 本地模型设为默认
    "status": "active",
    "config": json.dumps({"max_seq_len": 512})
})

# SCORE 类别
models_to_add.append({
    "name": "自定义评分模型API",
    "type": "api",
    "category": "SCORE",
    "provider": "自定义",
    "api_url": "",
    "api_key": "",
    "description": "自定义评分模型API端点",
    "is_default": True,
    "status": "active",
    "config": json.dumps({"method": "POST"})
})

models_to_add.append({
    "name": "本地评分规则引擎",
    "type": "local_program",
    "category": "SCORE",
    "provider": "本地",
    "command_path": "python",
    "command_args": "-m scoring_engine --config scoring_rules.json",
    "description": "基于规则引擎的本地评分系统",
    "is_default": True,  # 本地模型设为默认
    "status": "active",
    "config": json.dumps({"rules_file": "scoring_rules.json"})
})

# 先删除现有的模型（可选）
cursor.execute("DELETE FROM ai_models")

# 插入新模型
for model in models_to_add:
    cursor.execute("""
        INSERT INTO ai_models (
            name, type, category, provider, api_url, api_key,
            model_name, command_args, status, is_default, config, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        model["name"],
        model["type"],
        model["category"],
        model["provider"],
        model.get("api_url", ""),
        model.get("api_key", ""),
        model.get("model_name", ""),
        model.get("command_args", ""),
        model["status"],
        model["is_default"],
        model["config"],
        datetime.now().isoformat()
    ))

conn.commit()

# 验证插入的模型
cursor.execute("SELECT id, name, type, category, is_default FROM ai_models ORDER BY category, type")
models = cursor.fetchall()
print("Added models:")
for model in models:
    print(f"  ID: {model[0]}, Name: {model[1]}, Type: {model[2]}, Category: {model[3]}, Default: {model[4]}")

conn.close()
print(f"\nTotal {len(models_to_add)} models added successfully!")