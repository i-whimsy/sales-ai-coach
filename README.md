# AI 销售教练系统

AI Sales Coaching System 是一个基于人工智能的销售能力提升系统。销售人员可以上传自己的销售录音，系统会自动识别语音、多维度分析销售表现，并生成详细的评分和改进建议，帮助销售人员快速提升沟通和销售能力。

## ✨ 核心功能

### 🎤 录音上传与管理
- 支持 MP3、WAV、M4A 等常见音频格式
- 最大支持 200MB 文件上传
- 录音列表管理，支持重命名、删除等操作

### 🧠 智能语音识别
- 内置本地 Whisper 模型，无需网络即可完成语音转文字
- 支持中英文混合识别，准确率高达 95%+
- 自动区分说话人，识别停顿和语气词

### 📊 多维度智能分析
系统从五个维度对销售表现进行全面评估：
- **表达质量（20%）**：语速、流畅度、停顿、口头禅分析
- **内容完整度（30%）**：产品介绍、需求挖掘、方案呈现、价值传递完整性评估
- **逻辑结构（20%）**：沟通逻辑、流程合理性、说服力评估
- **客户理解度（20%）**：需求倾听、痛点挖掘、异议处理能力评估
- **说服力（10%）**：案例使用、价值表达、成交引导能力评估

### 📈 可视化报告
- 直观的评分仪表盘，多维度对比分析
- 详细的改进建议，针对性提升能力
- 支持报告导出和分享
- 历史记录对比，跟踪能力成长

### ⚙️ 灵活配置
- 自定义评分权重，适配不同行业销售场景
- 支持配置 OpenAI、Claude、DeepSeek 等多种大模型
- 本地运行，数据安全可控

### 💻 命令行工具 (CLI)
除了 Web 界面，还提供命令行工具进行本地分析：
```bash
cd cli
pip install -r requirements.txt

# 分析录音
python cli/main.py analyze audio.mp3

# 仅转写
python cli/main.py transcript audio.mp3

# 对比两个录音
python cli/main.py compare audio1.mp3 audio2.mp3
```

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Node.js 18+
- Windows / macOS / Linux

### 一键启动（推荐）
#### Windows
```batch
start-all.bat
```

#### macOS/Linux
```bash
chmod +x start-all.sh
./start-all.sh
```

### 手动启动

#### 1. 启动后端服务
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
后端服务将在 http://localhost:8000 启动

#### 2. 启动前端服务
```bash
cd frontend-vue
npm install
npm run dev
```
前端服务将在 http://localhost:3002 启动

### 访问系统
打开浏览器访问 http://localhost:3002 即可使用系统

## 📖 系统架构

```
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI 主程序
│   ├── database.py         # 数据库配置
│   ├── models.py           # 数据模型
│   ├── ai_analyzer.py      # AI 分析引擎
│   ├── speech_analysis.py  # 语音分析模块
│   └── requirements.txt    # Python 依赖
├── frontend-vue/           # Vue 前端
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── assets/         # 静态资源
│   │   └── main.js         # 入口文件
│   └── package.json        # Node.js 依赖
├── sales_coach.db          # SQLite 数据库（自动创建）
├── uploads/                # 上传文件存储
├── logs/                   # 日志文件存储
└── reports/                # 分析报告存储
```

## 🔧 API 接口

### 基础接口
- `GET /health` - 健康检查
- `GET /api/v1/recordings` - 获取录音列表
- `POST /api/v1/recordings` - 上传录音
- `POST /api/v1/recordings/{id}/analyze` - 分析录音
- `GET /api/v1/recordings/{id}` - 获取录音详情
- `DELETE /api/v1/recordings/{id}` - 删除录音

### 配置接口
- `GET /api/v1/api-config` - 获取 API 配置
- `POST /api/v1/api-config` - 更新 API 配置
- `GET /api/v1/scoring-config` - 获取评分配置
- `POST /api/v1/scoring-config` - 更新评分配置

## 🛠️ 技术栈

### 后端
- FastAPI - 高性能 Web 框架
- SQLAlchemy - ORM 框架
- SQLite - 轻量级数据库
- OpenAI Whisper - 语音识别
- 支持 OpenAI/Claude/DeepSeek 大模型

### 前端
- Vue 3 - 渐进式 JavaScript 框架
- Vite - 下一代前端构建工具
- Tailwind CSS - 实用优先的 CSS 框架
- Axios - HTTP 客户端

## 📝 更新日志

### v2.0.0 (2026-03-07)
- ✨ 全新 Vue 3 前端界面，更美观易用
- 🔧 修复数据库字段不匹配问题
- 🚀 优化 API 代理配置，解决跨域问题
- 📊 修复历史页面和详情页运行时错误
- ⚡ 提升整体性能和稳定性

## 🤝 贡献指南
欢迎提交 Issue 和 Pull Request 帮助改进项目。

## 📄 许可证
MIT License

---

## 🚀 项目介绍
AI 销售教练系统是由 OpenClaw 自主研发的智能销售能力提升平台，基于 FastAPI + Vue 3 技术栈构建，支持语音识别、多维度智能分析、自动评分等核心功能。

本项目完全开源，欢迎 Star 和 Fork！

