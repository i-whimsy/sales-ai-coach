# Sales Audio Analyzer CLI - 快速入门

## 项目已创建完成！✅

项目位置：`C:\Users\clawbot\.openclaw\workspace\projects\sales-audio-cli`

## 项目结构

```
sales-audio-cli/
├── cli.py                      # 主 CLI 程序
├── config.json                 # 配置文件
├── prompt_template.txt         # LLM Prompt 模板
├── requirements.txt            # Python 依赖
├── README.md                   # 完整文档
├── QUICKSTART.md              # 快速入门（本文件）
├── test_cli.py                # 测试脚本
│
└── modules/                   # 功能模块
    ├── audio_loader.py        # 音频加载
    ├── vad_analyzer.py        # 语音活动检测
    ├── speech_to_text.py      # Whisper 语音转文本
    ├── prosody_analyzer.py    # 韵律分析
    ├── emotion_analyzer.py    # 情绪识别
    ├── filler_detector.py     # 填充词检测
    ├── metrics_builder.py     # 指标构建
    └── json_exporter.py       # JSON 导出
```

## 安装步骤

### 1. 安装依赖

```bash
cd C:\Users\clawbot\.openclaw\workspace\projects\sales-audio-cli
pip install -r requirements.txt
```

**预计安装时间**：5-10 分钟（首次安装 PyTorch 较大）

### 2. 验证安装

```bash
python test_cli.py
```

### 3. 运行分析

```bash
python cli.py analyze your_audio.wav --output result.json
```

## 命令示例

### 基础分析
```bash
python cli.py analyze demo.wav
```

### 详细输出
```bash
python cli.py analyze demo.wav --verbose --show-progress
```

### 导出 LLM Prompt
```bash
python cli.py analyze demo.wav --export-llm-prompt
```

### 仅转录
```bash
python cli.py transcribe demo.wav -o transcript.txt
```

### 对比两个文件
```bash
python cli.py compare v1.wav v2.wav
```

## 输出说明

### 生成的文件

执行 `analyze` 命令后，会在 `outputs/{audio_name}/` 目录下生成：

1. **analysis_result.json** - 完整分析结果
2. **transcript.txt** - 转写文本（如果使用了 `--save-transcript`）
3. **llm_prompt.txt** - LLM Prompt（如果使用了 `--export-llm-prompt`）

### JSON 结构

```json
{
  "audio_info": { ... },         // 音频基础信息
  "vad_analysis": { ... },       // 语音活动分析
  "speech_metrics": { ... },     // 语速指标
  "prosody_metrics": { ... },    // 韵律特征
  "emotion_metrics": { ... },    // 情绪识别
  "transcript": { ... },         // 转写文本
  "filler_metrics": { ... },     // 填充词统计
  "processing_meta": { ... }     // 处理元数据
}
```

## 配置说明

### config.json

编辑 `config.json` 可以调整：

- **Whisper 模型大小**：`tiny/base/small/medium/large`
- **VAD 阈值**：0-1 之间
- **是否启用情绪识别**
- **输出格式**

### 性能优化

如果显存有限，可以：

1. 使用较小的 Whisper 模型（`--model base`）
2. 跳过情绪分析（`--no-emotion`）
3. 使用 CPU（在 config.json 中设置 `"device": "cpu"`）

## 典型工作流

### 销售培训场景

```bash
# 1. 分析销售录音
python cli.py analyze sales_call.wav \
  --output analysis.json \
  --export-llm-prompt \
  --verbose

# 2. 将以下两个文件发送给大模型：
#    - outputs/sales_call/analysis_result.json
#    - outputs/sales_call/llm_prompt.txt

# 3. 获取 AI 的评价和建议
```

### 批量分析

```bash
# Windows PowerShell
Get-ChildItem recordings/*.wav | ForEach-Object {
  python cli.py analyze $_.FullName --output "results/$($_.BaseName).json"
}
```

## 常见问题

### Q: 安装很慢怎么办？
A: 使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 提示找不到 torch 或 torchaudio？
A: 可能需要单独安装：
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Q: 情绪识别失败？
A: SpeechBrain 模型较大（~2GB），首次使用需要下载。可以使用 `--no-emotion` 跳过。

### Q: 中文识别不准？
A: 使用更大的 Whisper 模型：
```bash
python cli.py analyze demo.wav --model large
```

## 下一步

1. ✅ 项目已创建完成
2. ⏳ 安装依赖（`pip install -r requirements.txt`）
3. ⏳ 运行测试（`python test_cli.py`）
4. ⏳ 开始使用！

## 获取帮助

```bash
# 查看帮助
python cli.py --help
python cli.py analyze --help
```

---

**版本**: v0.1.0  
**创建时间**: 2026-03-08
