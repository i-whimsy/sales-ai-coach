# SalesCoach CLI 测试文档

## 测试环境准备

### 1.1 安装依赖

```bash
cd cli
pip install -r requirements.txt
```

### 1.2 验证安装

```bash
python main.py --version
```

## 测试语音文件

本测试使用 TTS (Text-to-Speech) 生成的测试语音。

测试语音内容：销售演示对话（约2分钟）

## 测试场景

### 场景1: 仅转写测试

**命令：**
```bash
python cli/main.py transcript cli/test_audio.mp3
```

**预期输出：**
- 生成 `outputs/test_audio/transcript.txt`
- 生成 `outputs/test_audio/transcript.json`

**验证：**
- 转写文本应该包含测试语音中的主要内容
- 语言检测应该正确（中文）

---

### 场景2: 完整分析测试

**命令：**
```bash
python cli/main.py analyze cli/test_audio.mp3 --model base
```

**预期输出：**
- Step 1/6: Speech to text
- Step 2/6: Speech analysis
- Step 3/6: Content analysis
- Step 4/6: Customer understanding analysis
- Step 5/6: Calculating scores
- Step 6/6: Generating report

**生成文件：**
- `outputs/test_audio/transcript.txt` - 转写文本
- `outputs/test_audio/speech_analysis.json` - 语音分析结果
- `outputs/test_audio/content_analysis.json` - 内容分析结果
- `outputs/test_audio/report.json` - 评分报告
- `outputs/test_audio/report.md` - Markdown报告

**验证分数范围：**
- Total Score: 0-100
- Expression: 0-100 (语速、流畅度)
- Content: 0-100 (内容完整度)
- Logic: 0-100 (逻辑结构)
- Customer: 0-100 (客户理解)
- Persuasion: 0-100 (说服力)

---

### 场景3: AI增强分析测试

**命令：**
```bash
python cli/main.py analyze cli/test_audio.mp3 --use-ai --api-key YOUR_OPENAI_KEY
```

**注意：** 需要设置 OpenAI API Key

```bash
export OPENAI_API_KEY=sk-xxxxxx
# 或
set OPENAI_API_KEY=sk-xxxxxx
```

---

### 场景4: 对比测试

**命令：**
```bash
python cli/main.py compare cli/test_audio.mp3 cli/test_audio2.mp3
```

**预期输出：**
- 两个录音的分数对比表格
- 内容覆盖度对比

---

## 测试结果示例

### 成功输出示例

```
SalesCoach Analysis
File: cli/test_audio.mp3
Model: base

Step 1/6: Speech to text
  Language: zh
  Duration: 120.50s
  Text length: 1850 chars
  Saved: outputs/test_audio/transcript.txt

Step 2/6: Speech analysis
  Expression score: 75.50
  Speaking rate: 150.00 wpm
  Pause frequency: 3.50/min
  Saved: outputs/test_audio/speech_analysis.json

Step 3/6: Content analysis
  Content score: 83.33
  Logic score: 70.00
  Saved: outputs/test_audio/content_analysis.json

Step 4/6: Customer understanding analysis

Step 5/6: Calculating scores

Step 6/6: Generating report

==================================================
Sales Coaching Report
==================================================

Total Score: 78.50

Dimension Scores
----------------------------------------
Dimension     Score    Weight
----------------------------------------
Expression    75.5     20%
Content       83.3     30%
Logic         70.0     20%
Customer      86.7     20%
Persuasion    77.5     10%
----------------------------------------

Strengths:
  ✓ 表达流畅，语速适中
  ✓ 内容涵盖面较广

Issues:
  - 逻辑结构需要改进

Suggestions:
  - 优化演讲结构，使用清晰的过渡
```

---

## 故障排查

### 问题1: whisper 模块未安装

**错误：**
```
ImportError: whisper not installed
```

**解决：**
```bash
pip install openai-whisper
```

### 问题2: ffmpeg 未安装

**错误：**
```
RuntimeError: ffmpeg not found
```

**解决：**
- Windows: 下载 ffmpeg.exe 并添加到 PATH
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

### 问题3: 模型文件下载失败

**解决：**
```bash
# 手动下载 Whisper 模型
python -c "import whisper; whisper.load_model('base')"
```

---

## 完整测试流程

```bash
# 1. 进入项目目录
cd sales-ai-coach

# 2. 进入CLI目录
cd cli

# 3. 安装依赖
pip install -r requirements.txt

# 4. 生成测试语音（如需要）
# 使用系统TTS或在线TTS生成测试音频

# 5. 运行测试
python main.py transcript test_audio.mp3

# 6. 查看结果
cat outputs/test_audio/transcript.txt
```

---

## 测试检查清单

- [ ] CLI 命令可以正常执行
- [ ] 转写功能正常生成文本
- [ ] 语音分析生成正确指标
- [ ] 内容分析识别关键点
- [ ] 评分计算正确
- [ ] 所有输出文件正常生成
- [ ] Markdown报告格式正确

---

## 性能基准

| 模型大小 | 转写速度 | 内存占用 |
|---------|---------|---------|
| tiny    | ~10x    | ~1GB    |
| base    | ~7x     | ~1.5GB  |
| small   | ~4x     | ~2.5GB  |
| medium  | ~2x     | ~5GB    |
| large   | 1x      | ~10GB   |

*速度指相对于实时播放时间的处理速度
