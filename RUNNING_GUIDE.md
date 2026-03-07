# 运行指南

## 📋 系统要求

### 最低配置
- CPU: 2核 2GHz+
- 内存: 4GB RAM
- 存储: 10GB 可用空间
- 系统: Windows 10+, macOS 10.15+, Linux (CentOS 7+/Ubuntu 18.04+)

### 推荐配置
- CPU: 4核 3GHz+
- 内存: 8GB RAM
- 存储: 20GB SSD
- 网络: 100Mbps 以上（首次使用需要下载模型）

---

## 🚀 部署方式

### 1. 本地开发部署
适合开发和测试使用，参考 `QUICK_START.md`。

### 2. 生产环境部署

#### 后端部署
```bash
# 1. 安装依赖
cd backend
pip install -r requirements.txt

# 2. 使用 Gunicorn 部署（Linux/macOS）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# 3. Windows 环境使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 前端部署
```bash
# 1. 构建生产版本
cd frontend-vue
npm install
npm run build

# 2. 部署 dist 目录到 Nginx 或其他静态服务器
# Nginx 配置示例：
server {
    listen 80;
    server_name your-domain.com;
    
    # 前端静态文件
    location / {
        root /path/to/frontend-vue/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # API 代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## ⚙️ 配置说明

### 后端配置
配置文件位于 `backend/config.py`：
```python
class Settings:
    PROJECT_NAME = "AI Sales Coaching System"
    VERSION = "2.0.0"
    DATABASE_URL = "sqlite:///./sales_coach.db"
    UPLOAD_DIR = "uploads"
    MAX_UPLOAD_SIZE = 200 * 1024 * 1024  # 200MB
```

### 前端配置
配置文件位于 `frontend-vue/vite.config.js`：
```javascript
export default defineConfig({
  server: {
    port: 3002,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  # 后端地址
        changeOrigin: true
      }
    }
  }
})
```

### 评分权重配置
可以在系统设置页面调整各维度的评分权重：
- 表达质量: 默认 20%
- 内容完整度: 默认 30%
- 逻辑结构: 默认 20%
- 客户理解度: 默认 20%
- 说服力: 默认 10%

---

## 🔧 模型配置

### 本地模型（默认）
系统内置本地 Whisper Base 模型，无需 API 密钥即可使用：
- **优点**：数据本地处理，安全可靠，无需网络
- **缺点**：识别准确率略低于云端模型，占用系统资源

#### 本地模型安装方法
系统会在首次运行时自动下载 Whisper Base 模型，也可以手动安装：
```bash
# 安装 whisper 依赖
pip install openai-whisper

# 手动下载模型（可选）
# 模型会自动下载到以下路径：
# Windows: C:\Users\用户名\.cache\whisper\base.pt
# macOS: ~/Library/Caches/whisper/base.pt
# Linux: ~/.cache/whisper/base.pt
```

#### 模型选择建议
| 模型大小 | 所需显存 | 识别速度 | 准确率 | 适用场景 |
|---------|---------|----------|--------|----------|
| tiny    | <1GB    | 极快     | 一般   | 实时语音识别，低配置机器 |
| base    | <1GB    | 快       | 良好   | 通用场景，默认选择 |
| small   | 2GB     | 中等     | 优秀   | 对准确率要求较高 |
| medium  | 5GB     | 慢       | 非常好 | 专业级分析，长录音 |
| large   | 10GB    | 极慢     | 最佳   | 企业级高精度需求 |

#### 切换模型版本
修改 `backend/speech_analysis.py` 中的模型名称：
```python
# 默认使用 base 模型
model = whisper.load_model("base")
# 切换为 small 模型
# model = whisper.load_model("small")
```

### 云端模型（推荐）
配置 API 密钥可以获得更好的分析效果：

#### OpenAI API
```
API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
支持 GPT-3.5-turbo、GPT-4 等模型，分析效果最佳。

#### Claude API
```
API Key: sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
适合长文本分析，逻辑推理能力强。

#### DeepSeek API
```
API Key: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
中文支持好，性价比高。

---

## 📊 数据管理

### 数据存储位置
- 数据库: `sales_coach.db`（SQLite 数据库文件）
- 上传文件: `uploads/` 目录
- 分析报告: `backend/reports/` 目录
- 日志文件: `logs/` 目录

### 数据备份
定期备份以下文件即可完成数据备份：
1. `sales_coach.db` - 数据库文件
2. `uploads/` 目录 - 上传的录音文件
3. `backend/reports/` 目录 - 分析报告

### 数据迁移
将备份文件复制到新环境的对应目录即可完成数据迁移。

---

## 🔒 安全建议

### 生产环境安全
1. 不要使用默认的 SQLite 数据库，建议切换到 PostgreSQL/MySQL
2. 配置 HTTPS，使用 SSL 证书加密传输
3. 开启身份认证，限制系统访问权限
4. 定期备份数据，防止数据丢失
5. 限制服务器端口对外暴露

### 数据安全
1. 录音文件和分析报告包含敏感信息，请妥善保管
2. 不要将系统部署在公网环境，建议企业内部使用
3. 定期清理过期数据，避免信息泄露

---

## 📈 性能优化

### 硬件优化
- 使用 SSD 存储可以大幅提升文件读写速度
- 增加内存可以提升大模型运行效率
- 多核 CPU 可以支持更多并发请求

### 软件优化
- 生产环境使用 Gunicorn/Uvicorn 多进程部署
- 配置 Nginx 反向代理提升静态资源访问速度
- 定期清理过期录音文件，释放存储空间
- 对于大流量场景，建议使用 Redis 做缓存

---

## ❌ 故障排除

### 后端相关问题

#### 问题：启动后端提示 ModuleNotFoundError
**解决方法：**
```bash
cd backend
pip install -r requirements.txt
```

#### 问题：数据库报错 "table xxx has no column named xxx"
**解决方法：**
```bash
# 备份数据后重新创建数据库
mv sales_coach.db sales_coach.db.backup
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

#### 问题：分析速度特别慢
**解决方法：**
1. 首次使用需要下载模型，请耐心等待
2. 增加系统内存，建议至少 8GB
3. 配置云端 API 密钥，使用云端模型分析

### 前端相关问题

#### 问题：前端页面无法访问
**解决方法：**
1. 检查前端服务是否正常启动
2. 确认端口 3002 没有被占用
3. 检查防火墙设置是否允许访问 3002 端口

#### 问题：前端请求后端失败
**解决方法：**
1. 检查后端服务是否正常启动
2. 确认 `frontend-vue/vite.config.js` 中的代理地址配置正确
3. 检查后端端口 8000 是否可以正常访问

#### 问题：上传文件失败
**解决方法：**
1. 检查文件大小是否超过 200MB 限制
2. 确认文件格式为 MP3/WAV/M4A
3. 检查 `uploads` 目录是否有写入权限

### 其他问题

#### 问题：语音识别准确率低
**解决方法：**
1. 录音质量差，建议在安静环境下录音
2. 语速过快或口音过重
3. 配置云端 API 可以提升识别准确率

#### 问题：评分结果不符合预期
**解决方法：**
1. 在系统设置页面调整评分权重
2. 提供更多行业语料对模型进行微调
3. 联系我们定制行业专属模型

---

## 📞 技术支持
如果遇到无法解决的问题，请提供以下信息：
1. 操作系统版本
2. Python 和 Node.js 版本
3. 错误截图和完整日志
4. 复现问题的操作步骤

