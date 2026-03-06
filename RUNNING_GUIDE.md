# AI销售教练系统 - 使用指南

## 🚀 快速启动

### Windows系统

**方法1：使用PowerShell脚本（推荐）**
```powershell
.
\start-all.ps1
```

**方法2：使用Batch脚本**
```cmd
start-all.bat
```

**停止服务**
```cmd
stop-all.bat
```

### Linux/macOS系统

**启动服务**
```bash
chmod +x start-all.sh stop-all.sh
./start-all.sh
```

**停止服务**
```bash
./stop-all.sh
```

## 📋 系统要求

- **Python** 3.8+ (推荐3.10+)
- **Node.js** 18+ (推荐20+)
- **npm** 或 **yarn** 包管理器
- **内存**：至少4GB RAM
- **磁盘空间**：至少5GB可用空间

## 🔧 手动安装与配置

### 1. 安装后端依赖

```bash
# 创建虚拟环境
python -m venv backend/venv

# 激活虚拟环境
# Windows
b\ackend\venv\Scripts\activate.bat

# Linux/macOS
source backend/venv/bin/activate

# 安装依赖
pip install -r backend/requirements.txt
```

### 2. 安装前端依赖

```bash
cd frontend
npm install
cd ..
```

### 3. 手动启动服务

#### 启动后端
```bash
# Windows
backend/venv/Scripts/activate.bat
python backend/main.py

# Linux/macOS
source backend/venv/bin/activate
python backend/main.py
```

#### 启动前端
```bash
cd frontend
npm run dev
```

## 🌐 访问地址

- **前端界面**：http://localhost:3000
- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health

## 📝 系统功能

### 主要功能

1. **📁 录音上传**
   - 支持MP3、WAV、M4A等格式
   - 实时上传进度显示
   - 文件大小限制：最大100MB

2. **🤖 AI分析**
   - 自动转录语音为文本
   - 分析表达能力、内容完整度、逻辑结构
   - 客户理解度和说服力评估
   - 生成综合评分和改进建议

3. **📊 报告查看**
   - 交互式雷达图展示各维度评分
   - 详细的优势分析和改进建议
   - 历史记录对比和趋势分析

4. **⚙️ 系统设置**
   - API密钥配置（OpenAI、DeepSeek、Anthropic）
   - 评分权重自定义
   - 系统参数调整

## 🛠️ 故障排除

### 常见问题

**1. 端口被占用**

如果端口被占用，可以修改配置文件中的端口号：
- 后端：修改`backend/config.py`中的`PORT`
- 前端：修改`frontend/package.json`中的启动命令

**2. 依赖安装失败**

```bash
# 清理并重新安装
pip cache purge
pip install -r backend/requirements.txt --no-cache-dir
```

**3. 后端启动失败**

检查日志文件：
```bash
# Windows
查看 logs\backend.log 和 logs\backend_error.log

# Linux/macOS
view logs/backend.log
```

**4. 前端页面无法访问**

检查前端日志：
```bash
# Windows
查看 logs\frontend.log 和 logs\frontend_error.log

# Linux/macOS
view logs/frontend.log
```

### 健康检查

1. **检查后端状态**
```bash
curl http://localhost:8000/health
```

2. **检查前端状态**
```bash
curl http://localhost:3000
```

## 📁 目录结构

```
sales-ai-coach/
├── backend/                 # 后端代码
│   ├── main.py             # 主入口文件
│   ├── requirements.txt    # Python依赖
│   ├── venv/               # 虚拟环境
│   ├── models.py           # 数据库模型
│   ├── speech_analysis.py  # 语音分析模块
│   └── ai_analyzer.py      # AI分析模块
├── frontend/               # 前端代码
│   ├── app/                # 应用页面
│   ├── components/         # React组件
│   ├── package.json        # Node.js依赖
│   └── next.config.js      # Next.js配置
├── logs/                   # 日志文件
├── start-all.ps1           # Windows启动脚本（PowerShell）
├── start-all.bat           # Windows启动脚本（Batch）
├── start-all.sh            # Linux/macOS启动脚本
├── stop-all.bat            # Windows停止脚本
├── stop-all.sh             # Linux/macOS停止脚本
└── RUNNING_GUIDE.md        # 使用指南
```

## 🔒 安全注意事项

1. **API密钥**：请勿在公共仓库提交包含API密钥的配置文件
2. **文件上传**：系统仅允许上传指定格式的音频文件
3. **网络安全**：生产环境建议配置HTTPS和访问控制
4. **数据备份**：定期备份重要数据和配置文件

## 📞 技术支持

如果遇到问题，请提供以下信息：
1. 操作系统版本
2. Python和Node.js版本
3. 错误日志文件内容
4. 重现步骤的详细描述

---

**🎉 祝您使用愉快！**