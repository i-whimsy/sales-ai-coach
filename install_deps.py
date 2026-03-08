#!/usr/bin/env python
import subprocess
import sys

packages = [
    "openai-whisper",
    "parselmouth"
]

for pkg in packages:
    print(f"Installing {pkg}...")
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", pkg, "-q",
        "--index-url", "https://pypi.tuna.tsinghua.edu.cn/simple"
    ])
    if result.returncode == 0:
        print(f"[OK] {pkg} installed")
    else:
        print(f"[FAIL] {pkg} failed")
