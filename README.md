# AI Sales Coaching System

AI Sales Coaching System 是一个企业内部使用的AI销售培训系统。销售人员可以上传自己的讲解录音，系统会自动识别语音、分析表达质量、评估讲解逻辑、模拟客户理解，并生成详细的评分报告，帮助企业评估销售讲解能力并提供优化建议。

## 🎉 最新更新 (2026-03-06)

### 1. 一键启动脚本
- 🚀 新增多平台一键启动脚本，支持 Windows、Linux、macOS
- 📦 自动环境检测、依赖安装、服务启动全流程自动化
- 📊 集成健康检查、日志管理、自动打开浏览器功能

### 2. 自动提交到GitHub
- 🔄 任务完成后自动将代码提交到GitHub远程仓库
- 📝 支持自定义提交信息
- 🔒 支持SSH和HTTPS两种认证方式

### 3. 完善的文档体系
- 📚 新增 `RUNNING_GUIDE.md` 详细使用指南
- 🛠️ 新增故障排除章节
- 📋 平台特定操作说明

### 4. 用户体验优化
- 🎨 改进前端界面设计，更美观易用
- 🔧 修复报告页面加载错误
- 📈 优化后端性能和稳定性

## 核心功能

### 1. 音频上传
- 支持拖拽上传音频文件
- 支持 MP3、WAV、M4A 格式
- 文件大小限制：最大 20MB

### 2. 自动语音识别
- 优先使用 OpenAI Whisper API 进行语音识别
- 备用方案：本地 Whisper 模型
- 自动转录录音内容

### 3. AI 讲解分析
- **表达能力分析**：分析语速、停顿、流畅度、口头禅
- **内容完整度分析**：检查是否包含公司介绍、行业问题、技术方案、核心优势、客户案例、商业价值
- **逻辑结构分析**：评估开场、问题引入、递进逻辑、总结
- **客户理解度分析**：模拟客户理解，回答关键问题
- **说服力分析**：评估是否使用案例、价值表达、是否引起兴趣

### 4. 自动评分
- 总分 100 分，五个维度评分：
  - 表达能力 20%
  - 内容完整度 30%
  - 逻辑结构 20%
  - 客户理解度 20%
  - 说服力 10%

### 5. 生成分析报告
- 可视化评分雷达图
- 详细的优缺点分析
- 具体的改进建议
- 历史记录和报告对比

### 6. API 集成
- 支持 OpenAI API
- 支持 DeepSeek API
- 支持 Anthropic Claude API
- 支持 OpenAI Whisper API

## 技术架构

### 前端
- **框架**：Next.js 14
- **语言**：TypeScript
- **样式**：TailwindCSS
- **UI组件**：Shadcn UI
- **图表库**：Recharts
- **图标**：Lucide React

### 后端
- **框架**：FastAPI
- **语言**：Python 3.8+
- **数据库**：SQLite
- **语音识别**：Whisper (本地 + API)
- **依赖**：See `backend/requirements.txt`

## 项目结构

```
sales-ai-coach/
├── backend/                 # 后端代码
│   ├── main.py             # 主应用入口
│   ├── ai_analyzer.py      # AI分析模块
│   ├── speech_analysis.py  # 语音分析模块
│   ├── config.py          # 配置管理
│   ├── database.py        # 数据库连接
│   ├── models.py          # 数据模型
│   └── requirements.txt   # Python依赖
├── frontend/               # 前端代码
│   ├── app/               # Next.js应用
│   │   ├── page.tsx       # 首页
│   │   ├── upload/        # 上传页面
│   │   ├── analyze/       # 分析页面
│   │   ├── report/        # 报告页面
│   │   ├── history/       # 历史记录
│   │   └── settings/      # 设置页面
│   ├── components/        # React组件
│   ├── lib/              # 工具函数
│   └── package.json       # 前端依赖
├── logs/                   # 日志文件
├── RUNNING_GUIDE.md       # 详细使用指南
├── start-all.bat          # Windows Batch启动脚本
├── start-all.ps1          # Windows PowerShell启动脚本
├── start-all.sh           # Linux/macOS启动脚本
├── stop-all.bat           # Windows停止脚本
├── stop-all.sh            # Linux/macOS停止脚本
└── README.md             # 项目说明
```

## 🚀 一键启动 (推荐)

### Windows系统
```powershell
# 使用PowerShell（推荐）
.
\start-final.ps1

# 或者使用Batch脚本
start-all.bat
```

### Linux/macOS系统
```bash
# 添加执行权限
chmod +x start-all.sh stop-all.sh

# 启动服务
./start-all.sh
```

### 停止服务
```powershell
# Windows系统
.
\stop-all.bat

# Linux/macOS系统
./stop-all.sh
```

## 🛠️ 手动安装和运行

### 1. 环境要求
- Python 3.8 或更高版本
- Node.js 18 或更高版本
- npm 或 yarn

### 2. 后端安装和运行

```bash
cd sales-ai-coach/backend

# 创建虚拟环境（可选但推荐）
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行后端服务器
python main.py
```

后端服务器将在 `http://localhost:8000` 启动。

### 3. 前端安装和运行

```bash
cd sales-ai-coach/frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

前端应用将在 `http://localhost:3000` 启动。

## 系统页面

### 1. 首页
- 系统介绍
- 功能说明
- 快速操作按钮

### 2. 上传页面
- 文件拖拽上传
- 文件类型验证
- 上传进度显示

### 3. 分析进度页面
- 实时显示分析进度
- 各阶段状态说明

### 4. 分析报告页面
- 总评分展示
- 维度评分雷达图
- 详细分析报告
- 优点和改进建议

### 5. 历史记录页面
- 所有分析记录列表
- 报告快速访问
- 统计信息展示

### 6. 设置页面
- API Key 配置
- 系统参数设置

## API 接口文档

启动后端服务器后，访问以下地址查看API文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 使用注意事项

1. **API Key 配置**：
   - 首次使用需要在设置页面配置 API Key
   - 支持 OpenAI、DeepSeek、Claude、Whisper API

2. **文件格式**：
   - 支持 MP3、WAV、M4A 格式
   - 文件大小不超过 20MB
   - 建议录音质量为 44.1kHz 或 48kHz

3. **分析时间**：
   - 分析时间取决于录音时长和服务器性能
   - 一般 1 分钟的录音需要 30-60 秒分析时间

4. **报告保存**：
   - 分析报告会自动保存到服务器
   - 支持下载和分享

## 开发说明

### 添加新分析维度

编辑 `backend/ai_analyzer.py` 文件，在 `generate_report` 方法中添加新的分析逻辑。

### 前端组件开发

使用 Shadcn UI 组件库，所有组件位于 `frontend/components/ui/` 目录。

### 数据库修改

编辑 `backend/models.py` 文件，然后运行以下命令更新数据库：

```bash
python -c "from database import engine; import models; models.Base.metadata.create_all(bind=engine)"
```

## 🔄 自动提交到GitHub

系统会在每次完成任务后自动将代码提交到GitHub。您也可以手动运行：

```powershell
# Windows系统
.
\commit-to-github.ps1 -message "您的提交信息"

# Linux/macOS系统
./commit-to-github.sh "您的提交信息"
```

## 许可证

MIT License

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub: https://github.com/i-whimsy/sales-ai-coach
- Email: contact@example.com
