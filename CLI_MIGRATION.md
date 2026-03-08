# CLI 迁移说明

## 迁移日期
2026-03-08

## 变更内容

### 删除的模块
- ❌ `cli/` - 旧 CLI（功能简单）
- ❌ `core/` - 旧核心模块

### 新增的模块
- ✅ `modules/` - 新的模块化分析工具
  - `audio_loader.py` - 音频加载（支持 m4a/mp3/wav）
  - `vad_analyzer.py` - VAD 语音活动检测
  - `speech_to_text.py` - Whisper 转录
  - `prosody_analyzer.py` - 韵律分析（音高、能量、语速）
  - `emotion_analyzer.py` - 情绪识别（可选）
  - `filler_detector.py` - 填充词检测
  - `metrics_builder.py` - 指标构建
  - `json_exporter.py` - JSON 导出

### 新增的命令工具
- ✅ `sales_audio_cli.py` - 新的 CLI 工具

## 使用方式变更

### 旧 CLI (已删除)
```bash
python cli/main.py analyze audio.wav
```

### 新 CLI (当前)
```bash
# 方式 1：直接运行
python sales_audio_cli.py analyze audio.wav

# 方式 2：作为模块
python -m modules audio.wav
```

## 功能对比

| 功能 | 旧 CLI | 新 CLI |
|------|--------|--------|
| 音频格式支持 | wav | wav/m4a/mp3 |
| VAD 分析 | ❌ | ✅ |
| 韵律分析 | ❌ | ✅ |
| 填充词检测 | ❌ | ✅ |
| 情绪识别 | ❌ | ✅ (可选) |
| JSON 输出 | 简单 | 结构化 |
| LLM Prompt | ❌ | ✅ |
| 对比分析 | ✅ | ✅ |

## 迁移步骤

1. ✅ 删除旧 `cli/` 和 `core/` 目录
2. ✅ 迁移 `sales-audio-cli` 所有内容到 `sales-ai-coach`
3. ✅ 重命名 `cli.py` 为 `sales_audio_cli.py`
4. ✅ 更新文档

## 依赖变更

### 新增依赖
```bash
pip install librosa soundfile parselmouth pydantic
```

### 保留依赖
```bash
pip install openai-whisper click tqdm torch torchaudio
```

## 向后兼容

旧 CLI 的命令不再可用。如需兼容，可以创建符号链接或包装脚本。

---

**迁移完成时间**: 2026-03-08 14:15  
**执行人**: OpenClaw Agent
