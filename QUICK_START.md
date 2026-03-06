# AI Sales Coaching System v2.0.0 - Quick Start Guide

## 🚀 快速开始

### 方法一：一键启动所有服务（推荐）

```cmd
start-all-services.bat
```

这个脚本会：
1. 检查系统环境（Python、Node.js）
2. 自动安装所有依赖
3. 启动后端服务器（端口8000）
4. 启动前端服务器（端口3000）
5. 自动打开浏览器

### 方法二：分别启动服务

**启动后端**
```cmd
start-backend.bat
```

**启动前端**
```cmd
start-frontend.bat
```

### 方法三：手动启动

**后端**
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python new_app.py
```

**前端**
```cmd
cd frontend
npm install
npm run dev
```

## 🎯 系统特性

### ✅ 已实现的功能

1.  **录音上传**
   - ✅ 支持MP3、WAV、M4A等格式
   - ✅ 自动文件类型验证
   - ✅ 安全的文件存储

2.  **AI分析**
   - ✅ 模拟AI分析报告生成
   - ✅ 智能评分系统（5个维度）
   - ✅ 详细的优缺点分析
   - ✅ 实用的改进建议

3.  **数据管理**
   - ✅ 完整的CRUD操作
   - ✅ 历史记录管理
   - ✅ 报告存储和查询

4.  **系统配置**
   - ✅ API密钥管理
   - ✅ 评分权重设置
   - ✅ 健康检查端点

5.  **API文档**
   - ✅ 自动生成Swagger文档
   - ✅ ReDoc文档支持
   - ✅ 详细的API说明

## 🌐 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端界面 | http://localhost:3000 | 用户操作界面 |
| 后端API | http://localhost:8000 | API接口地址 |
| API文档 | http://localhost:8000/docs | Swagger文档 |
| 健康检查 | http://localhost:8000/health | 服务状态检查 |

## 📋 API端点

### 录音管理
- `POST /api/v1/recordings` - 上传录音文件
- `GET /api/v1/recordings` - 获取所有录音
- `GET /api/v1/recordings/{id}` - 获取单个录音
- `DELETE /api/v1/recordings/{id}` - 删除录音

### AI分析
- `POST /api/v1/recordings/{id}/analyze` - 分析录音

### 系统配置
- `GET /api/v1/api-config` - 获取API配置
- `POST /api/v1/api-config` - 更新API配置
- `GET /api/v1/scoring-config` - 获取评分配置
- `POST /api/v1/scoring-config` - 更新评分配置

### 健康检查
- `GET /health` - 服务健康检查

## 🛠️ 技术架构

### 后端
- **框架**：FastAPI 0.109.0
- **语言**：Python 3.8+
- **文件存储**：本地文件系统
- **数据存储**：内存数据库（可扩展至SQLite/MySQL）
- **并发**：异步API设计

### 前端
- **框架**：Next.js 14
- **语言**：TypeScript
- **样式**：TailwindCSS
- **UI组件**：Shadcn UI
- **图表库**：Recharts

## 🎨 系统界面

### 主要页面
1.  **首页** - 系统概览和快速操作
2.  **上传页面** - 录音文件上传
3.  **分析页面** - 实时分析进度
4.  **报告页面** - 详细分析报告
5.  **历史记录** - 所有录音列表
6.  **设置页面** - 系统配置

### 特色功能
- ✅ 交互式雷达图评分展示
- ✅ 完整的报告下载功能
- ✅ 响应式设计，支持移动端
- ✅ 实时进度条展示
- ✅ 友好的错误提示

## 🚀 性能优化

### 后端优化
- ✅ 异步IO处理
- ✅ 轻量级设计，启动快速
- ✅ 内存数据存储，查询迅速
- ✅ 自动依赖管理

### 前端优化
- ✅ Next.js自动代码分割
- ✅ 静态资源优化
- ✅ 组件懒加载
- ✅ API请求缓存

## 🛡️ 安全特性

- ✅ 文件类型验证
- ✅ 安全的文件存储
- ✅ 输入数据验证
- ✅ CORS配置
- ✅ 错误信息脱敏

## 📊 数据格式

### 分析报告结构
```json
{
  "total_score": 85.5,
  "expression_score": 88.2,
  "content_score": 82.1,
  "logic_score": 86.7,
  "customer_score": 83.4,
  "persuasion_score": 89.2,
  "strengths": ["优点1", "优点2"],
  "improvements": ["改进1", "改进2"],
  "transcript": "录音文本...",
  "analysis_date": "2026-03-07T12:00:00Z"
}
```

## 🔄 版本更新

### v2.0.0 (2026-03-07)
- ✅ 重写整个后端，简化架构
- ✅ 使用内存数据库替代SQLite
- ✅ 移除复杂的依赖
- ✅ 增强的错误处理
- ✅ 更简洁的API设计
- ✅ 完整的类型定义
- ✅ 改进的部署脚本

## 📞 技术支持

### 常见问题

**Q: 后端启动失败？**
A: 检查Python版本是否>=3.8，网络连接是否正常

**Q: 前端页面无法加载？**
A: 检查Node.js版本是否>=18，端口3000是否被占用

**Q: 报告生成失败？**
A: 检查录音文件是否损坏，格式是否正确

### 调试技巧

1.  **查看服务日志** - 每个服务都有独立的控制台输出
2.  **健康检查** - 访问http://localhost:8000/health
3.  **API测试** - 使用Swagger文档测试API
4.  **浏览器调试** - 使用Chrome DevTools查看前端错误

## 📈 未来规划

- [ ] 数据库持久化（SQLite/MySQL）
- [ ] 真实AI集成（OpenAI API）
- [ ] 用户认证系统
- [ ] 多人协作功能
- [ ] 数据分析面板
- [ ] 实时推送通知
- [ ] 邮件报告发送
- [ ] Docker容器化

---

**🎊 祝您使用愉快！**