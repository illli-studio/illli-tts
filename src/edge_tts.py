"""Edge TTS 引擎模块 - 无需下载模型"""

import asyncio
import edge_tts
import os
from pathlib import Path
from typing import Optional, Union
import numpy as np
import soundfile as sf


class EdgeTTSEngine:
    """Edge TTS 引擎 - 使用微软 Edge 在线语音"""
    
    # 语音映射
    VOICES = {
        "female_young": "zh-CN-XiaoxiaoNeural",      # 晓晓 - 年轻女声
        "male_young": "zh-CN-YunxiNeural",           # 云希 - 年轻男声
        "female_mature": "zh-CN-XiaoyouNeural",      # 晓悠 - 成熟女声
        "male_mature": "zh-CN-YunyangNeural",        # 云扬 - 成熟男声
        "female_child": "zh-CN-XiaoxiaoNeural",      # 儿童
        "male_child": "zh-CN-YunhaoNeural",          # 云浩 - 儿童
    }
    
    def __init__(self):
        self.device = "edge-tts"  # 在线服务
    
    async def _speak_async(
        self,
        text: str,
        voice: str = "female_young",
        rate: str = "+0%",
        pitch: str = "+0Hz",
        output_path: str = "/tmp/edge-tts-output.mp3"
    ) -> str:
        """异步生成语音"""
        voice_name = self.VOICES.get(voice, self.VOICES["female_young"])
        
        communicate = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch)
        await communicate.save(output_path)
        
        return output_path
    
    def speak(
        self,
        text: str,
        voice: str = "female_young",
        speed: float = 1.0,
        ref_audio: Optional[str] = None,
        voice_desc: Optional[str] = None,
        output_file: str = "/tmp/illli-edge-output.mp3"
    ) -> str:
        """生成语音 (同步接口)"""
        # 转换速度到 rate
        if speed != 1.0:
            rate = f"{int((speed - 1) * 100)}%"
        else:
            rate = "+0%"
        
        # 运行异步函数
        asyncio.run(self._speak_async(text, voice, rate, "+0Hz", output_file))
        
        return output_file
    
    def speak_to_audio(self, text: str, voice: str = "female_young", speed: float = 1.0) -> np.ndarray:
        """生成语音并返回 numpy 数组"""
        mp3_path = self.speak(text, voice, speed)
        
        # 转换 MP3 到 numpy
        import subprocess
        # 使用 ffmpeg 转换为 WAV，然后读取
        wav_path = mp3_path.replace(".mp3", ".wav")
        subprocess.run([
            "ffmpeg", "-y", "-i", mp3_path, "-ar", "24000", "-ac", "1", wav_path
        ], check=True, capture_output=True)
        
        audio, sr = sf.read(wav_path)
        
        # 清理临时文件
        Path(mp3_path).unlink(missing_ok=True)
        Path(wav_path).unlink(missing_ok=True)
        
        return audio
    
    def save(self, audio_or_path, path: Union[str, Path]):
        """保存音频"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果是字符串路径，直接复制
        if isinstance(audio_or_path, str):
            import shutil
            shutil.copy(audio_or_path, path)
        else:
            # 是 numpy 数组
            sf.write(str(path), audio_or_path, 24000)


# 同步接口函数
def speak(text: str, voice: str = "female_young", speed: float = 1.0, output_path: str = "/tmp/edge-output.mp3") -> str:
    """快捷函数"""
    engine = EdgeTTSEngine()
    return engine.speak(text, voice, speed, output_file=output_path)


if __name__ == "__main__":
    # 测试
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "你好，我是小灵"
    voice = sys.argv[2] if len(sys.argv) > 2 else "female_young"
    
    print(f"🎵 生成语音: {text}")
    output = speak(text, voice)
    print(f"✅ 已保存到: {output}")
