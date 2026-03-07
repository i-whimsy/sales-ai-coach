"""
本地模型安装和检测工具
"""

import os
import subprocess
import sys
from pathlib import Path

class ModelInstaller:
    """本地模型安装和检测类"""
    
    @staticmethod
    def get_whisper_models_dir():
        """获取Whisper模型存储目录"""
        if sys.platform == "win32":
            return Path(os.path.expanduser("~")) / ".cache" / "whisper"
        elif sys.platform == "darwin":
            return Path(os.path.expanduser("~")) / "Library" / "Caches" / "whisper"
        else:  # Linux
            return Path(os.path.expanduser("~")) / ".cache" / "whisper"
    
    @staticmethod
    def list_installed_models():
        """列出已安装的本地模型"""
        models_dir = ModelInstaller.get_whisper_models_dir()
        models = []
        
        if models_dir.exists():
            for file in models_dir.glob("*.pt"):
                model_name = file.stem
                size_mb = round(file.stat().st_size / (1024 * 1024), 2)
                models.append({
                    "name": model_name,
                    "path": str(file),
                    "size_mb": size_mb,
                    "installed": True
                })
        
        return models
    
    @staticmethod
    def install_whisper_model(model_name: str):
        """安装Whisper模型"""
        valid_models = ["tiny", "base", "small", "medium", "large"]
        if model_name not in valid_models:
            return {
                "success": False,
                "message": f"无效的模型名称，可选模型: {', '.join(valid_models)}"
            }
        
        try:
            # 检查是否已安装
            models_dir = ModelInstaller.get_whisper_models_dir()
            model_path = models_dir / f"{model_name}.pt"
            
            if model_path.exists():
                return {
                    "success": True,
                    "message": f"模型 {model_name} 已安装",
                    "path": str(model_path)
                }
            
            # 创建目录
            models_dir.mkdir(parents=True, exist_ok=True)
            
            # 使用whisper下载模型
            cmd = [sys.executable, "-m", "pip", "install", "openai-whisper"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "message": f"安装whisper依赖失败: {result.stderr}"
                }
            
            # 下载模型
            cmd = [sys.executable, "-c", f"import whisper; whisper.load_model('{model_name}')"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {
                    "success": False,
                    "message": f"下载模型失败: {result.stderr}"
                }
            
            return {
                "success": True,
                "message": f"模型 {model_name} 安装成功",
                "path": str(model_path)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"安装失败: {str(e)}"
            }
    
    @staticmethod
    def uninstall_whisper_model(model_name: str):
        """卸载Whisper模型"""
        try:
            models_dir = ModelInstaller.get_whisper_models_dir()
            model_path = models_dir / f"{model_name}.pt"
            
            if not model_path.exists():
                return {
                    "success": False,
                    "message": f"模型 {model_name} 未安装"
                }
            
            model_path.unlink()
            
            return {
                "success": True,
                "message": f"模型 {model_name} 已卸载"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"卸载失败: {str(e)}"
            }
    
    @staticmethod
    def check_model_availability(model_name: str):
        """检查模型是否可用"""
        try:
            models_dir = ModelInstaller.get_whisper_models_dir()
            model_path = models_dir / f"{model_name}.pt"
            
            if not model_path.exists():
                return {
                    "available": False,
                    "message": f"模型 {model_name} 未安装",
                    "install_command": f"pip install openai-whisper && python -c \"import whisper; whisper.load_model('{model_name}')\""
                }
            
            # 测试模型加载
            import whisper
            model = whisper.load_model(model_name)
            del model  # 释放内存
            
            return {
                "available": True,
                "message": f"模型 {model_name} 可用",
                "path": str(model_path)
            }
            
        except Exception as e:
            return {
                "available": False,
                "message": f"模型不可用: {str(e)}",
                "install_command": f"pip install openai-whisper && python -c \"import whisper; whisper.load_model('{model_name}')\""
            }
