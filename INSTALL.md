# 安装指南

## 快速安装（推荐）

### Windows 用户

```bash
# 1. 进入项目目录
cd C:\Users\clawbot\.openclaw\workspace\projects\sales-audio-cli

# 2. 安装核心依赖（CPU 版本，约 5-10 分钟）
pip install numpy torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 3. 安装其他依赖
pip install librosa soundfile openai-whisper parselmouth click tqdm pydantic

# 4. 验证安装
python -c "import torch; print(f'PyTorch {torch.__version__} installed successfully')"
```

### 使用 GPU（可选）

如果有 NVIDIA GPU：

```bash
# 安装 CUDA 版本
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 分步安装说明

### 步骤 1：核心科学计算库

```bash
pip install numpy
```

**时间**：1-2 分钟  
**大小**：~15MB

### 步骤 2：PyTorch

```bash
# CPU 版本（推荐）
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU 版本（需要 NVIDIA GPU）
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**时间**：5-10 分钟  
**大小**：CPU ~200MB, GPU ~2GB

### 步骤 3：音频处理库

```bash
pip install librosa soundfile parselmouth
```

**时间**：2-3 分钟  
**大小**：~50MB

### 步骤 4：Whisper

```bash
pip install openai-whisper
```

**时间**：3-5 分钟  
**大小**：~500MB（包含模型）

### 步骤 5：其他依赖

```bash
pip install click tqdm pydantic
```

**时间**：1 分钟  
**大小**：~5MB

## 验证安装

```bash
python test_cli.py
```

应该看到：
```
============================================================
Sales Audio Analyzer CLI - Test Suite
============================================================

Testing AudioLoader...
  Duration: 2.00s
  Sample rate: 16000 Hz
  ✓ AudioLoader test passed
...
Tests complete: 7 passed, 0 failed
```

## 常见问题

### Q1: numpy 安装失败

**错误**：`Failed to build 'numpy'`

**解决**：
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用预编译的 wheel
pip install numpy --only-binary :all:
```

### Q2: torch 下载慢

**解决**：使用清华镜像
```bash
pip install torch --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 找不到 ffmpeg

**错误**：`ffmpeg not found`

**解决**：
```bash
# Windows (使用 chocolatey)
choco install ffmpeg

# 或下载 ffmpeg.exe 并添加到 PATH
# https://ffmpeg.org/download.html
```

### Q4: 显存不足

**解决**：
1. 使用 CPU 模式
2. 使用较小的 Whisper 模型（`--model tiny` 或 `base`）
3. 跳过情绪分析（`--no-emotion`）

## 最小化安装

如果只需要基础功能：

```bash
# 只安装核心依赖
pip install numpy torch librosa soundfile openai-whisper click tqdm

# 跳过情绪识别（SpeechBrain 很大）
# 使用时加上 --no-emotion 参数
```

## 完整安装

```bash
pip install -r requirements.txt
```

## 安装后测试

```bash
# 运行测试套件
python test_cli.py

# 或快速测试
python -c "from modules import *; print('All modules imported successfully')"
```

---

**预计总安装时间**：10-15 分钟  
**磁盘空间需求**：~2GB（CPU 版本）或 ~4GB（GPU 版本）
