"""模型下载管理模块"""

import os
from pathlib import Path
from typing import Optional, List
from tqdm import tqdm

from .config import Config


class ModelManager:
    """模型下载管理器"""
    
    MODEL_IDS = {
        # ModelScope 模型
        "modelscope": "qwen/Qwen3-TTS-1.7B",
        # HuggingFace 模型 - 支持 CustomVoice 的版本
        "huggingface": "Qwen/Qwen3-TTS-1.7B"
    }
    
    # 需要下载的文件列表
    MODEL_FILES = [
        "config.json",
        "model.safetensors",
        "tokenizer.json",
        "vocab.txt"
    ]
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.cache_dir = Path(self.config.cache_dir).expanduser()
        self.model_dir = self.cache_dir / self.config.model_name
    
    def is_model_downloaded(self) -> bool:
        """检查模型是否已下载"""
        if not self.model_dir.exists():
            return False
        
        # 检查关键文件是否存在
        for f in self.MODEL_FILES:
            if not (self.model_dir / f).exists():
                return False
        return True
    
    def download(self, source: Optional[str] = None) -> str:
        """下载模型"""
        source = source or self.config.download_source
        
        if source == "modelscope":
            return self._download_from_modelscope()
        elif source == "huggingface":
            return self._download_from_huggingface()
        else:
            raise ValueError(f"Unknown source: {source}")
    
    def _download_from_modelscope(self) -> str:
        """从 ModelScope 下载模型"""
        try:
            from modelscope.hub.snapshot_download import snapshot_download
            
            print(f"📥 从 ModelScope 下载: {self.MODEL_IDS['modelscope']}")
            
            model_dir = snapshot_download(
                self.MODEL_IDS["modelscope"],
                cache_dir=str(self.cache_dir)
            )
            
            print(f"✅ 模型已下载到: {model_dir}")
            return model_dir
            
        except ImportError:
            print("⚠️ ModelScope 未安装，尝试使用 HuggingFace...")
            return self._download_from_huggingface()
    
    def _download_from_huggingface(self) -> str:
        """从 HuggingFace 下载模型"""
        try:
            from huggingface_hub import snapshot_download
            
            print(f"📥 从 HuggingFace 下载: {self.MODEL_IDS['huggingface']}")
            
            model_dir = snapshot_download(
                self.MODEL_IDS["huggingface"],
                cache_dir=str(self.cache_dir)
            )
            
            print(f"✅ 模型已下载到: {model_dir}")
            return model_dir
            
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            raise
    
    def get_model_path(self) -> Optional[Path]:
        """获取模型路径"""
        if self.is_model_downloaded():
            return self.model_dir
        return None
    
    def list_local_models(self) -> List[str]:
        """列出本地缓存的模型"""
        if not self.cache_dir.exists():
            return []
        
        models = []
        for item in self.cache_dir.iterdir():
            if item.is_dir() and item.name.startswith("Qwen"):
                models.append(item.name)
        return models
