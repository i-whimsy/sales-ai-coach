import sqlite3
import json

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# Clear existing data
cursor.execute("DELETE FROM task_model_configs")
cursor.execute("DELETE FROM ai_models")

# Default prompts for each task
default_prompts = {
    '语音转写': '请将以下音频转录为文字：{transcript}',
    '内容分析': '请分析以下销售对话的内容完整性和逻辑结构：{transcript}',
    '情感识别': '请识别以下语音的情感倾向：{transcript}',
    '说话人识别': '请识别以下音频中的说话人身份：{transcript}',
    '意图识别': '请识别以下对话中的客户意图：{transcript}',
    '质量评分': '请对以下销售对话进行综合评分：{transcript}'
}

# Insert tasks with proper encoding
tasks = [
    ('语音转写', '将音频转换为文字', json.dumps(['语音识别', '多语言'])),
    ('内容分析', '分析内容完整性和逻辑', json.dumps(['自然语言处理', '内容分析'])),
    ('情感识别', '识别语音情感倾向', json.dumps(['情感分析', '自然语言处理'])),
    ('说话人识别', '识别说话人身份', json.dumps(['声纹识别', '语音识别'])),
    ('意图识别', '识别客户意图', json.dumps(['自然语言处理', '意图识别'])),
    ('质量评分', '综合评分', json.dumps(['评分模型', '自然语言处理']))
]

for task in tasks:
    cursor.execute("""
        INSERT INTO task_model_configs (task_name, description, required_tags, is_active, prompt_config)
        VALUES (?, ?, ?, 1, ?)
    """, (task[0], task[1], task[2], default_prompts.get(task[0], '')))

# Insert models with proper encoding
models = [
    # ASR
    ("OpenAI Whisper API", "api", "ASR", "OpenAI", "https://api.openai.com/v1/audio/transcriptions", "whisper-1", "OpenAI官方语音识别API，支持多语言，高准确率", 1),
    ("本地 Whisper (faster-whisper)", "local_program", "ASR", "本地", "", "base", "本地faster-whisper模型，无需API，支持中文", 1),
    
    # NLP
    ("OpenAI GPT-4o", "api", "NLP", "OpenAI", "https://api.openai.com/v1/chat/completions", "gpt-4o", "OpenAI最新多模态模型，强大的自然语言理解能力", 1),
    ("本地 Ollama Llama3", "local_service", "NLP", "Ollama", "http://localhost:11434/api/generate", "llama3:8b", "本地Ollama运行的Llama3模型，支持中文", 1),
    
    # EMOTION
    ("百度情感分析API", "api", "EMOTION", "百度", "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify", "", "百度AI情感分析API，支持中文文本情感识别", 1),
    ("本地情感分析模型", "local_program", "EMOTION", "本地", "", "", "基于RoBERTa的中文情感分析模型", 1),
    
    # VOICEPRINT
    ("讯飞声纹识别API", "api", "VOICEPRINT", "讯飞", "https://api.xfyun.cn/v1/service/v1/iat", "", "讯飞声纹识别API，支持说话人识别", 1),
    ("本地声纹识别", "local_program", "VOICEPRINT", "本地", "", "", "基于SpeechBrain的声纹识别模型", 1),
    
    # INTENT
    ("阿里云意图识别", "api", "INTENT", "阿里云", "https://nlp.cn-shanghai.aliyuncs.com/v2/intent", "", "阿里云自然语言处理API，支持意图识别", 1),
    ("本地意图识别模型", "local_program", "INTENT", "本地", "", "", "基于ERNIE的中文意图识别模型", 1),
    
    # SCORE
    ("自定义评分模型API", "api", "SCORE", "自定义", "", "", "自定义评分模型API端点", 1),
    ("本地评分规则引擎", "local_program", "SCORE", "本地", "", "", "基于规则引擎的本地评分系统", 1)
]

for model in models:
    cursor.execute("""
        INSERT INTO ai_models (name, type, category, provider, api_url, model_name, is_default, status, config, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'active', '{}', datetime('now'))
    """, (model[0], model[1], model[2], model[3], model[4], model[5], model[7]))

conn.commit()

# Verify
print("=== Tasks ===")
cursor.execute("SELECT task_name, prompt_config FROM task_model_configs")
for task in cursor.fetchall():
    print(f"  {task[0]}: {task[1][:30] if task[1] else 'None'}...")

print("\n=== Models ===")
cursor.execute("SELECT id, name, category FROM ai_models")
for model in cursor.fetchall():
    print(f"  ID {model[0]}: {model[1]} ({model[2]})")

conn.close()
print("\nDone!")