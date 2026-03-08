# AI Sales Coaching System - Architecture Documentation

## 1. System Overview
AI Sales Coaching System is a web application that analyzes sales recordings to provide coaching feedback using AI. The system consists of a Python FastAPI backend, a Vue 3 frontend, and a CLI tool, designed to help sales professionals improve their communication skills through AI-driven analysis.

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        SalesCoach System                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐                    │
│  │   Web Frontend  │    │   CLI Tool      │                    │
│  │   (Vue 3 + Vite)│    │   (Click)       │                    │
│  │   Port: 3002    │    │   Commands      │                    │
│  └────────┬────────┘    └────────┬────────┘                    │
│           │                      │                              │
│           └──────────┬───────────┘                              │
│                      ▼                                          │
│           ┌─────────────────────┐                               │
│           │    Backend API     │                               │
│           │    (FastAPI)       │                               │
│           │    Port: 8001      │                               │
│           └──────────┬──────────┘                               │
│                      │                                          │
│           ┌──────────▼──────────┐                               │
│           │    Shared Core     │◄──── cli/core/ 移动到这里      │
│           │    (core/)         │                               │
│           │  - speech_to_text  │                               │
│           │  - speech_analysis │                               │
│           │  - content_analysis│                               │
│           │  - scoring         │                               │
│           └─────────────────────┘                               │
│                      │                                          │
│           ┌──────────▼──────────┐                               │
│           │   SQLite Database  │                               │
│           │  (sales_coach.db)  │                               │
│           └─────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Directory Structure

```
sales-ai-coach/
├── core/                      # ⭐ 共享核心模块 (NEW!)
│   ├── __init__.py
│   ├── config.py              # 共享配置
│   ├── speech_to_text.py     # 语音转文本
│   ├── speech_analysis.py     # 表达分析
│   ├── content_analysis.py    # 内容分析
│   └── scoring.py             # 评分引擎
│
├── backend/                   # Web后端
│   ├── main.py               # FastAPI主应用
│   ├── models.py             # SQLAlchemy模型
│   ├── database.py           # 数据库连接
│   ├── config.py             # 后端配置
│   ├── ai_analyzer.py        # AI分析器
│   ├── speech_analysis.py    # ⚠️ 遗留，引用core/
│   ├── model_manager.py      # 模型管理
│   ├── model_installer.py    # 本地模型安装
│   └── uploads/              # 上传文件目录
│
├── cli/                      # CLI工具
│   ├── main.py              # Click命令行入口
│   ├── config.py            # CLI配置
│   ├── core/                # ⚠️ 移动到 core/
│   │   ├── speech_to_text.py
│   │   ├── speech_analysis.py
│   │   ├── content_analysis.py
│   │   └── scoring.py
│   └── requirements.txt
│
├── frontend-vue/            # Web前端
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   └── components/      # 公共组件
│   └── package.json
│
├── docs/                    # 文档
├── outputs/                  # CLI输出目录
└── sales_coach.db          # SQLite数据库
```

## 4. Module Responsibilities

### 4.1 Core Modules (core/)

所有分析逻辑统一放在 `core/` 目录，Web后端和CLI共享使用：

| Module | Responsibility |
|--------|----------------|
| `config.py` | 共享配置（权重、评分规则、checklist等） |
| `speech_to_text.py` | 语音转文本（Whisper封装） |
| `speech_analysis.py` | 表达分析（语速、停顿、流畅度） |
| `content_analysis.py` | 内容分析（完整性、逻辑结构、关键词检测） |
| `scoring.py` | 评分引擎（多维度加权计算） |

### 4.2 Backend Modules (backend/main.py)

- **Server Setup**: FastAPI server with CORS enabled
- **Database**: SQLite with SQLAlchemy ORM
- **Model Management** (`model_manager.py`): 统一模型管理，支持在线/本地模型
- **API Endpoints**:
  - `/health` - 健康检查
  - `/api/v1/recordings` - 录音管理CRUD
  - `/api/v1/recordings/:id/analyze` - AI分析录音
  - `/api/v1/models` - 模型管理CRUD
  - `/api/v1/models/call` - 统一模型调用接口
  - `/api/v1/tasks` - 任务配置管理
  - `/api/v1/api-config` - API密钥管理
  - `/api/v1/scoring-config` - 评分权重配置

### 4.3 CLI Modules (cli/main.py)

| Command | Description |
|---------|-------------|
| `analyze` | 完整分析流程：转录→表达分析→内容分析→评分→报告 |
| `transcript` | 仅语音转文本 |
| `compare` | 对比两个录音的分析结果 |

### 4.4 Frontend Views

- `Home.vue` -  Landing page
- `Upload.vue` - 文件上传 + 模型选择
- `History.vue` - 录音历史列表
- `Analyze.vue` - 分析进度
- `Report.vue` - 详细分析报告
- `Settings.vue` - 系统配置
- `ModelManagement.vue` - 模型管理
- `LogViewer.vue` - 日志查看

## 5. Data Flow

### 5.1 CLI Analysis Flow
```
audio file → speech_to_text → transcript
                              ↓
                         speech_analysis → expression metrics
                              ↓
                         content_analysis → content/logic scores
                              ↓
                         scoring → final scores + report
                              ↓
                         outputs/{name}/
```

### 5.2 Web Analysis Flow
```
upload → /api/v1/recordings → database
                                   ↓
                        /api/v1/recordings/:id/analyze
                                   ↓
                        speech_to_text (backend)
                                   ↓
                        core.speech_analysis
                                   ↓
                        ai_analyzer (AI增强)
                                   ↓
                        scoring + report_json
                                   ↓
                        database → frontend display
```

## 6. Model Configuration

### 6.1 模型分类
- **在线模型 (online)**: OpenAI Whisper, GPT-4o, DeepSeek, 字节跳动等
- **本地模型 (local)**: Whisper Base/Small/Medium等本地部署模型

### 6.2 模型类别
- ASR(语音识别), NLP(自然语言处理), EMOTION(情感分析), VOICEPRINT(声纹识别), INTENT(意图识别), SCORE(评分模型)

### 6.3 统一模型调用
- **POST /api/v1/models/call**: 根据任务名称自动选择合适的模型

## 7. Technology Stack

### Backend
- Python + FastAPI + SQLAlchemy + SQLite + Uvicorn

### Frontend
- Vue 3 + Vue Router + Vite + Tailwind CSS + Axios + Lucide Icons

### CLI
- Python + Click

### AI/ML
- Whisper (本地/在线) for speech-to-text
- OpenAI GPT / DeepSeek for AI-enhanced analysis

## 8. Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Expression | 20% | 语速、停顿、流畅度 |
| Content | 30% | 内容完整性 |
| Logic | 20% | 逻辑结构 |
| Customer | 20% | 客户理解 |
| Persuasion | 10% | 说服力 |

## 9. Configuration

### 9.1 CLI Config (cli/config.py, core/config.py)
```python
DEFAULT_WEIGHTS = {
    "expression": 0.20,
    "content": 0.30,
    "logic": 0.20,
    "customer": 0.20,
    "persuasion": 0.10
}

CONTENT_CHECKLIST = ["公司介绍", "行业问题", "技术方案", "核心优势", "客户案例", "商业价值"]
STRUCTURE_CHECKLIST = ["开场白", "问题引入", "逻辑流", "总结"]
```

### 9.2 Backend Config (backend/config.py)
```python
DATABASE_URL = "sqlite:///./sales_coach.db"
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB
```

## 10. Future Enhancements

- Integration with real AI transcription and analysis services
- User authentication and authorization
- Team collaboration features
- Advanced analytics and reporting
- Integration with CRM systems
- Mobile application support
