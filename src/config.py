"""配置管理模块"""

import os
from pathlib import Path
from typing import Any, Optional
import yaml


class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        "model": {
            "name": "Qwen3-TTS-1.7B-CustomVoice",
            "download_source": "modelscope",  # modelscope / huggingface
            "cache_dir": "./models"
        },
        "tts": {
            "default_language": "zh",
            "default_speed": 1.0,
            "default_voice": "female_young"
        },
        "voices": {
            "female_young": {
                "name": "年轻女性",
                "description": "温柔甜美的女声"
            },
            "male_young": {
                "name": "年轻男性",
                "description": "清澈干净的男声"
            },
            "female_mature": {
                "name": "成熟女性",
                "description": "成熟稳重的女声"
            },
            "male_mature": {
                "name": "成熟男性",
                "description": "成熟稳重的男声"
            }
        },
        "feishu": {
            "enabled": True,
            "default_target": "self"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.illli-tts/config.yaml")
        self.config = self._load()
    
    def _load(self) -> dict:
        """加载配置"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f) or {}
            # 合并默认配置和用户配置
            config = self.DEFAULT_CONFIG.copy()
            self._merge(config, user_config)
            return config
        return self.DEFAULT_CONFIG.copy()
    
    def _merge(self, base: dict, update: dict):
        """递归合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点号分隔的键"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self):
        """保存配置到文件"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, allow_unicode=True)
    
    @property
    def model_name(self) -> str:
        return self.get("model.name")
    
    @property
    def cache_dir(self) -> str:
        return self.get("model.cache_dir")
    
    @property
    def download_source(self) -> str:
        return self.get("model.download_source")
