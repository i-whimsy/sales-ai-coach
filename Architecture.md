# AI Sales Coaching System - Architecture Documentation

## 1. System Overview
AI Sales Coaching System is a web application that analyzes sales recordings to provide coaching feedback using AI. The system consists of a Python FastAPI backend and a Vue 3 frontend, designed to help sales professionals improve their communication skills through AI-driven analysis.

## 2. System Architecture
The system follows a typical client-server architecture:
- **Frontend**: Vue 3 application with Vite build tool, using Tailwind CSS for styling and Vue Router for navigation (运行在端口 3002)
- **Backend**: Python FastAPI providing REST API endpoints (运行在端口 8001)
- **Data Storage**: SQLite database (sales_coach.db)
- **AI Integration**: Support for both online models (OpenAI, DeepSeek, 字节跳动) and local models (Whisper)

## 3. Main Modules & Responsibilities

### 3.1 Backend Modules (main.py - FastAPI)
- **Server Setup**: FastAPI server with CORS enabled
- **Database**: SQLite with SQLAlchemy ORM
- **Model Management** (`model_manager.py`): 统一模型管理，支持在线/本地模型
- **Local Model Installer** (`model_installer.py`): 本地模型安装/卸载/检测
- **API Endpoints**:
  - `/health` - 健康检查
  - `/api/v1/recordings` - 录音管理CRUD
  - `/api/v1/recordings/:id/analyze` - AI分析录音
  - `/api/v1/models` - 模型管理CRUD
  - `/api/v1/models/call` - 统一模型调用接口
  - `/api/v1/models/:id/test` - 测试模型可用性
  - `/api/v1/tasks` - 任务配置管理
  - `/api/v1/tags` - 标签管理
  - `/api/v1/api-config` - API密钥管理
  - `/api/v1/scoring-config` - 评分权重配置

### 3.2 Frontend Modules
- **App Layout**: Main application structure with header, navigation menu, and footer
- **Views**:
  - `Home.vue` - Landing page with system introduction
  - `Upload.vue` - File upload with model selection
  - `History.vue` - List of previously uploaded recordings
  - `Analyze.vue` - Analysis progress interface
  - `Report.vue` - Detailed analysis report with scores and feedback
  - `Settings.vue` - System configuration for API keys and scoring weights
  - `ModelManagement.vue` - 模型管理页面（新增）
- **UI Components**: Reusable UI components (tabs, buttons, etc.)

## 4. Key Data Flow

### 4.1 Recording Upload Flow
1. User selects or drags a recording file in the frontend
2. Frontend validates file format and size (supports MP3, WAV, M4A; max 200MB)
3. Frontend sends POST request to `/api/v1/recordings` with file data
4. Backend creates recording entry and returns ID
5. Frontend displays success message with options to view history or start analysis

### 4.2 Recording Analysis Flow
1. User clicks "Analyze" on a recording in history
2. Frontend sends POST request to `/api/v1/recordings/:id/analyze`
3. Backend simulates AI analysis delay
4. Backend returns mock analysis report with scores and feedback
5. Frontend navigates to report page to display detailed results

## 5. Model Configuration & Call Logic

### 5.1 模型系统架构
- **AIModel**: 核心模型表，支持在线/本地模型分类
  - 字段: id, name, type, category, provider, api_url, api_key, model_name, local_path, status, is_default
- **ModelTag**: 模型标签表，用于模型分类
- **ModelTagRelation**: 模型-标签关联表
- **TaskModelConfig**: 任务模型配置表，定义不同任务使用的模型

### 5.2 模型分类
- **在线模型 (online)**: OpenAI Whisper, GPT-4o, DeepSeek, 字节跳动等
- **本地模型 (local)**: Whisper Base/Small/Medium等本地部署模型
- **模型类别**: ASR(语音识别), NLP(自然语言处理), EMOTION(情感分析), VOICEPRINT(声纹识别), INTENT(意图识别), SCORE(评分模型)

### 5.3 统一模型调用接口
- **POST /api/v1/models/call**: 根据任务名称自动选择合适的模型
- 支持指定模型ID或自动匹配
- 根据任务配置的required_tags匹配可用模型

### 5.4 分析流程
1. 用户上传录音时选择模型（或使用默认模型）
2. 模型ID保存在Recording.model_id字段
3. 分析时使用选定的模型进行语音转写和分析
4. 支持在线模型和本地模型的动态切换

## 6. Frontend-Backend Relationship
- **Communication**: Frontend uses Axios to make HTTP requests to backend REST API
- **CORS**: Backend is configured with CORS to allow cross-origin requests from frontend
- **Deployment**: Frontend can be deployed separately or served by the backend Express server
- **Responsiveness**: Frontend is built with responsive design principles to work on desktop and mobile devices

## 7. Important Design Decisions

### 7.1 Mock-First Development
- The system provides a complete mock backend to enable frontend development without requiring AI API keys or paid services
- Mock data closely mimics expected production responses

### 7.2 Modular Architecture
- Frontend components are organized by feature for maintainability
- Backend endpoints are grouped by resource type (RESTful design)

### 7.3 User Experience Focus
- File upload with drag-and-drop support and real-time validation
- Progress indicators for upload and analysis processes
- Clear visual hierarchy and responsive design with Tailwind CSS
- Intuitive navigation with clear call-to-action buttons

### 7.4 Configurable System
- API key management for different AI service providers
- Customizable scoring weights to adapt to different business needs
- Extensible design to support additional AI models in the future

## 8. Technology Stack

### 8.1 Backend
- **Python**: Runtime environment
- **FastAPI**: Web application framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (可切换到PostgreSQL/MySQL)
- **Uvicorn**: ASGI server

### 8.2 Frontend
- **Vue 3**: Progressive JavaScript framework with Composition API
- **Vue Router**: Client-side routing
- **Vite**: Build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **Lucide Vue Next**: Icon library

## 9. Latest Updates (2026-03-07)

### 9.1 模型管理系统
- 新增模型管理页面 (ModelManagement.vue)
- 支持模型的增删改查
- 支持模型测试和激活/停用
- 支持按类型、类别、状态筛选

### 9.2 模型选择集成到上传流程
- 上传页面新增模型选择下拉框
- 支持选择在线模型或本地模型
- 选择的模型ID保存到Recording.model_id
- 分析时使用用户选择的模型

### 9.3 后端更新
- Recording模型新增model_id字段
- /api/v1/recordings接口支持model_id参数
- /api/v1/recordings/:id/analyze使用选定模型
- 新增统一模型调用接口 /api/v1/models/call
- 模型初始化脚本 init_model_system.py

### 9.4 数据库表结构
- **AIModel**: 模型表 (13个预置模型)
- **ModelTag**: 标签表 (12个预置标签)
- **ModelTagRelation**: 模型-标签关联
- **TaskModelConfig**: 任务配置表 (6个预置任务)
- **Recording**: 录音表 (新增model_id字段)

## 10. Future Enhancements
- Integration with real AI transcription and analysis services
- Persistent database storage for recordings and reports
- User authentication and authorization
- Team collaboration features
- Advanced analytics and reporting
- Integration with CRM systems
- Mobile application support
