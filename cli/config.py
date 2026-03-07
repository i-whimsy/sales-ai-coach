"""
Configuration for SalesCoach CLI
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Default scoring weights
DEFAULT_WEIGHTS = {
    "expression": 0.20,
    "content": 0.30,
    "logic": 0.20,
    "customer": 0.20,
    "persuasion": 0.10
}

# AI API configurations
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")

# Whisper model size
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large

# Content checklist for analysis
CONTENT_CHECKLIST = [
    "公司介绍",
    "行业问题",
    "技术方案",
    "核心优势",
    "客户案例",
    "商业价值"
]

# Structure checklist
STRUCTURE_CHECKLIST = [
    "开场白",
    "问题引入",
    "逻辑流",
    "总结"
]

# Customer understanding questions
CUSTOMER_QUESTIONS = [
    "这家公司在做什么？",
    "解决了什么问题？",
    "为什么这个方案更好？",
    "是否产生了兴趣？"
]

def get_output_dir(audio_name: str) -> Path:
    """Get output directory for an audio file"""
    name_without_ext = Path(audio_name).stem
    output_dir = OUTPUTS_DIR / name_without_ext
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
