"""音色管理模块"""

from typing import Dict, Optional
from .config import Config


class VoiceManager:
    """音色管理器"""
    
    # 内置音色
    BUILT_IN_VOICES = {
        "female_young": {
            "name": "年轻女性",
            "description": "温柔甜美的女声",
            "voice_desc": "young female voice, sweet and gentle"
        },
        "male_young": {
            "name": "年轻男性",
            "description": "清澈干净的男声",
            "voice_desc": "young male voice, clear and clean"
        },
        "female_mature": {
            "name": "成熟女性",
            "description": "成熟稳重的女声",
            "voice_desc": "mature female voice, stable and composed"
        },
        "male_mature": {
            "name": "成熟男性",
            "description": "成熟稳重的男声",
            "voice_desc": "mature male voice, deep and stable"
        },
        "female_child": {
            "name": "小女孩",
            "description": "可爱的小女孩声音",
            "voice_desc": "little girl voice, cute and lively"
        },
        "male_child": {
            "name": "小男孩",
            "description": "可爱的小男孩声音",
            "voice_desc": "little boy voice, cute and energetic"
        }
    }
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
    
    def list_voices(self) -> Dict:
        """列出所有可用音色"""
        # 合并内置音色和用户配置
        voices = self.BUILT_IN_VOICES.copy()
        
        # 添加用户配置的音色
        user_voices = self.config.get("voices", {})
        voices.update(user_voices)
        
        return voices
    
    def get_voice(self, voice_id: str) -> Optional[Dict]:
        """获取指定音色信息"""
        voices = self.list_voices()
        return voices.get(voice_id)
    
    def get_voice_description(self, voice_id: str) -> Optional[str]:
        """获取音色的文字描述"""
        voice = self.get_voice(voice_id)
        if voice:
            return voice.get("voice_desc")
        return None
    
    def add_custom_voice(
        self,
        voice_id: str,
        name: str,
        description: str,
        voice_desc: str = None,
        ref_audio: str = None
    ):
        """添加自定义音色"""
        voices = self.config.get("voices", {})
        voices[voice_id] = {
            "name": name,
            "description": description,
            "voice_desc": voice_desc,
            "ref_audio": ref_audio
        }
        self.config.set("voices", voices)
        self.config.save()
    
    def validate_voice(self, voice_id: str) -> bool:
        """验证音色是否有效"""
        return voice_id in self.list_voices()
