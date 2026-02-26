"""illli-tts: 基于 Qwen3-TTS 的 CLI 文字转语音工具"""

__version__ = "0.1.0"
__author__ = "illli Studio"

from .tts import TTSEngine
from .models import ModelManager
from .voices import VoiceManager
from .sender import FeishuSender

__all__ = ["TTSEngine", "ModelManager", "VoiceManager", "FeishuSender"]
