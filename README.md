# AI Sales Coaching System

## 项目介绍

AI Sales Coaching System 是一个企业内部使用的AI销售培训系统。销售人员可以上传自己的讲解录音，系统会自动进行语音识别、AI讲解分析、自动评分并生成分析报告，帮助企业评估销售讲解能力并给出优化建议。

## 核心功能

### 1. 音频上传
- 支持 MP3、WAV、M4A 格式
- 拖拽上传，简单易用

### 2. 自动语音识别
- 优先使用 OpenAI Whisper API
- 备用方案：本地 Whisper 模型
- 高精度语音识别和转录

### 3. AI 讲解分析
系统会对销售讲解进行多维度分析：

#### 表达能力（20%）
- 语速
- 停顿
- 流畅度
- 口头禅检测

#### 内容完整度（30%）
检查是否包含：
- 公司介绍
- 行业问题
- 技术方案
- 核心优势
- 客户案例
- 商业价值

#### 逻辑结构（20%）
- 是否有清晰开场
- 是否有问题引入
- 是否有递进逻辑
- 是否有总结

#### 客户理解度（20%）
模拟普通客户回答：
- 这家公司是做什么的
- 产品解决什么问题
- 为什么比别人好
- 是否愿意继续了解

#### 说服力（10%）
- 是否有案例
- 是否有价值表达
- 是否让人产生兴趣

### 4. 自动评分
总分 100 分，每个维度权重可配置

### 5. 生成分析报告
包含详细的：
- 总评分
- 评分雷达图
- 优点
- 问题
- 改进建议

### 6. 历史记录
保存所有分析记录，随时查看和对比

### 7. API Key 设置
支持以下 API：
- OpenAI (GPT + Whisper)
- Anthropic Claude
- DeepSeek

## 技术架构

### 前端
- **Next.js 14**
- **React 18**
- **TypeScript**
- **Tailwind CSS**
- **Shadcn UI**

设计风格：简洁、高级、企业级（参考 Notion / Linear / Apple 风格）

### 后端
- **Python 3.11+**
- **FastAPI**
- **FastAPI CORSMiddleware**

### 数据库
- **SQLite** (轻量级，内置)

### AI 接口
- OpenAI API
- Anthropic API
- DeepSeek API

### 语音识别
- OpenAI Whisper API (优先)
- Local Whisper Model (备用)

## 安装和运行

### 1. 克隆项目
```bash
git clone https://github.com/i-whimsy/sales-ai-coach.git
cd sales-ai-coach
```

### 2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 启动后端服务
```bash
cd backend
python main.py
```
后端服务将在 http://localhost:8000 启动

### 4. 安装前端依赖
```bash
cd frontend
npm install
```

### 5. 启动前端开发服务器
```bash
cd frontend
npm run dev
```
前端将在 http://localhost:3000 启动

## 使用说明

1. **访问系统**：打开浏览器访问 http://localhost:3000
2. **上传录音**：点击 "上传录音" 按钮或拖拽音频文件到上传区域
3. **等待分析**：系统会自动进行语音识别和 AI 分析
4. **查看报告**：分析完成后会显示详细的分析报告和评分
5. **管理历史**：在 "历史记录" 页面查看所有分析过的录音
6. **API 配置**：在 "设置" 页面配置所需的 API Key

## 项目结构

```
sales-ai-coach/
├── backend/
│   ├── main.py                    # FastAPI 主应用
│   ├── ai_analyzer.py            # AI 分析模块
│   ├── speech_analysis.py        # 语音分析模块
│   ├── config.py                 # 配置管理
│   ├── database.py               # 数据库连接
│   ├── models.py                 # 数据模型
│   └── requirements.txt          # 依赖列表
├── frontend/
│   ├── app/
│   │   ├── layout.tsx            # 布局组件
│   │   ├── page.tsx              # 首页
│   │   ├── upload/
│   │   ├── progress/
│   │   ├── report/
│   │   ├── history/
│   │   └── settings/
│   ├── components/
│   │   ├── ui/                  # 基础 UI 组件
│   │   ├── Navbar.tsx
│   │   ├── Upload.tsx
│   │   └── Features.tsx
│   ├── public/
│   └── package.json
├── docs/
├── README.md
└── LICENSE
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License