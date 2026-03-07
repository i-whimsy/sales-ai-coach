# 快速开始指南

## 🎯 30秒快速启动

### Windows 用户
双击运行 `start-all.bat`，系统会自动完成所有配置并打开浏览器。

### macOS/Linux 用户
在终端执行：
```bash
./start-all.sh
```

## 📋 手动启动步骤

如果一键启动失败，可以按照以下步骤手动启动：

---

### 第一步：启动后端服务

1. 进入后端目录
```bash
cd backend
```

2. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 启动后端服务
```bash
python main.py
```

后端服务启动成功后会显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

### 第二步：启动前端服务

1. 进入前端目录
```bash
cd frontend-vue
```

2. 安装依赖
```bash
npm install
```

3. 启动前端服务
```bash
npm run dev
```

前端服务启动成功后会显示：
```
VITE v5.4.21 ready in xxx ms
➜ Local:   http://localhost:3002/
```

---

### 第三步：访问系统

打开浏览器访问 http://localhost:3002 即可开始使用。

## 💡 首次使用配置

1. 首次进入系统，建议先访问 **系统设置** 页面：
   - 配置 OpenAI/Claude/DeepSeek API 密钥（可选，本地模式可跳过）
   - 调整评分权重以适配您的业务场景

2. 点击 **上传录音** 页面，上传您的第一个销售录音进行测试。

## 🔍 常见问题

### Q: 后端启动失败，提示端口被占用
A: 请关闭占用 8000 端口的程序，或者修改 `backend/main.py` 中的端口配置。

### Q: 前端启动失败，提示端口被占用
A: 请关闭占用 3002 端口的程序，或者修改 `frontend-vue/vite.config.js` 中的端口配置。

### Q: 上传文件失败
A: 请检查文件大小是否超过 200MB，文件格式是否为 MP3/WAV/M4A。

### Q: 分析速度慢
A: 首次分析需要下载模型，建议保持网络畅通。后续分析会快很多。

### Q: 没有 API 密钥可以使用吗？
A: 可以，系统内置本地 Whisper 模型，不需要 API 密钥也可以完成基础的语音识别和分析功能。配置 API 密钥可以获得更准确的 AI 分析结果。

## 📞 技术支持
如果遇到其他问题，请查看 `RUNNING_GUIDE.md` 获取更详细的使用说明。
