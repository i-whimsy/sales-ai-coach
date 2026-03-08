# Sales Audio Analyzer CLI

客观语音指标提取工具 - 用于销售讲解音频分析

## 特点

- ✅ **只做客观指标提取**，不做主观评价
- ✅ **结构化 JSON 输出**，供大模型二次分析
- ✅ **8 大类指标**：音频信息、VAD、语速、韵律、情绪、填充词等
- ✅ **模块化设计**，易于扩展
- ✅ **支持多种模型**：Whisper、Silero VAD、SpeechBrain

## 安装

```bash
# 进入项目目录
cd sales-audio-cli

# 安装依赖
pip install -r requirements.txt
```

### 系统要求

- Python 3.8+
- PyTorch 2.0+
- 建议：NVIDIA GPU（加速 Whisper 和 SpeechBrain）

## 快速开始

### 基础分析

```bash
python cli.py analyze demo.wav
```

### 完整选项

```bash
python cli.py analyze demo.wav \
  --config config.json \
  --output result.json \
  --model large \
  --show-progress \
  --save-transcript \
  --verbose \
  --export-llm-prompt
```

### 仅转录

```bash
python cli.py transcribe demo.wav -o transcript.txt
```

### 对比分析

```bash
python cli.py compare v1.wav v2.wav
```

## 输出格式

### JSON 结构

```json
{
  "audio_info": {
    "duration_seconds": 185,
    "sample_rate": 16000,
    "file_size_mb": 2.8
  },
  "vad_analysis": {
    "speech_duration": 150,
    "silence_duration": 35,
    "speech_ratio": 0.81,
    "pause_count": 23,
    "avg_pause_duration": 1.1
  },
  "speech_metrics": {
    "words_total": 820,
    "words_per_minute": 266
  },
  "prosody_metrics": {
    "pitch_mean_hz": 145,
    "pitch_std_hz": 28,
    "energy_mean": 0.24,
    "energy_cv": 0.33
  },
  "emotion_metrics": {
    "dominant_emotion": "neutral",
    "confidence": 0.73
  },
  "transcript": {
    "text": "完整转写文本...",
    "model": "whisper-base"
  },
  "filler_metrics": {
    "filler_word_count": 18,
    "filler_ratio": 0.021,
    "fillers_per_100_words": 2.2
  },
  "processing_meta": {
    "timestamp": "2026-03-08T12:00:00",
    "pipeline_version": "0.1.0"
  }
}
```

### LLM Prompt

使用 `--export-llm-prompt` 时生成：

```
你是一个销售培训专家。

下面是一次销售讲解的客观语音分析数据...

分析数据如下：
{
  "audio_info": {...},
  "vad_analysis": {...},
  ...
}
```

## 配置

### config.json

```json
{
  "models": {
    "speech_to_text": {
      "provider": "whisper",
      "model": "base",
      "device": "auto"
    },
    "vad": {
      "provider": "silero",
      "threshold": 0.5
    },
    "emotion": {
      "provider": "speechbrain",
      "model": "emotion-recognition-wav2vec2"
    }
  },
  "audio_analysis": {
    "enable_pitch": true,
    "enable_energy": true,
    "enable_pause": true,
    "enable_jitter": true,
    "enable_shimmer": true
  },
  "features": {
    "enable_emotion": true,
    "enable_jitter_shimmer": true,
    "skip_if_too_long": 3600
  }
}
```

## 指标说明

### 1. 音频基础信息
- `duration_seconds`: 音频时长（秒）
- `sample_rate`: 采样率（Hz）
- `file_size_mb`: 文件大小（MB）

### 2. VAD 分析
- `speech_ratio`: 语音占比
- `pause_count`: 停顿次数
- `avg_pause_duration`: 平均停顿时长
- `long_pause_count`: 长停顿（>2s）次数

### 3. 语速指标
- `words_total`: 总词数
- `words_per_minute`: 每分钟词数（WPM）

### 4. 韵律特征
- `pitch_mean_hz`: 平均音高（Hz）
- `pitch_range_hz`: 音高范围（Hz）
- `energy_cv`: 能量变异系数

### 5. 情绪识别
- `dominant_emotion`: 主导情绪
- `confidence`: 置信度
- `emotion_probabilities`: 各情绪概率

### 6. 填充词
- `filler_word_count`: 填充词总数
- `fillers_per_100_words`: 每 100 词填充词数

## 项目结构

```
sales-audio-cli/
├── cli.py                  # 主 CLI 入口
├── config.json             # 配置文件
├── prompt_template.txt     # LLM Prompt 模板
├── requirements.txt        # Python 依赖
│
├── modules/
│   ├── __init__.py
│   ├── audio_loader.py     # 音频加载
│   ├── vad_analyzer.py     # VAD 分析
│   ├── speech_to_text.py   # 语音转文本
│   ├── prosody_analyzer.py # 韵律分析
│   ├── emotion_analyzer.py # 情绪识别
│   ├── filler_detector.py  # 填充词检测
│   ├── metrics_builder.py  # 指标构建
│   └── json_exporter.py    # JSON 导出
│
└── outputs/                # 输出目录
    └── {audio_name}/
        ├── analysis_result.json
        ├── transcript.txt
        └── llm_prompt.txt
```

## 典型工作流

### 1. 销售培训场景

```bash
# 分析销售录音
python cli.py analyze sales_call.wav \
  --output analysis.json \
  --export-llm-prompt

# 将 JSON + Prompt 发送给大模型
# 获取评价和建议
```

### 2. 批量分析

```bash
# 对多个文件进行分析
for file in recordings/*.wav; do
  python cli.py analyze "$file" --output "results/$(basename "$file" .wav).json"
done

# 汇总结果进行对比
```

### 3. A/B 测试

```bash
# 对比两个版本
python cli.py compare v1.wav v2.wav

# 查看哪个版本语速更合适、填充词更少
```

## 性能优化

### GPU 加速

在 `config.json` 中配置：

```json
{
  "performance": {
    "use_gpu": true,
    "batch_size": 16
  }
}
```

### 跳过耗时分析

```bash
# 跳过情绪分析（SpeechBrain 模型较大）
python cli.py analyze demo.wav --no-emotion
```

## 常见问题

### Q: Whisper 模型下载慢？
A: 使用镜像或手动下载模型到 `~/.cache/whisper/`

### Q: 情绪识别失败？
A: SpeechBrain 需要较多显存，可使用 `--no-emotion` 跳过

### Q: 中文识别不准？
A: 使用 `whisper-large-v3` 模型，或指定 `--model large`

## License

MIT

## 版本

- v0.1.0 - 初始版本
