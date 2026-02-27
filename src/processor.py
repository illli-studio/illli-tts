"""音频后处理模块"""

import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional


class AudioProcessor:
    """音频后处理"""
    
    @staticmethod
    def adjust_speed(audio: np.ndarray, speed: float) -> np.ndarray:
        """调整语速"""
        import librosa
        return librosa.effects.time_stretch(audio, rate=speed)
    
    @staticmethod
    def adjust_pitch(audio: np.ndarray, semitones: float, sr: int = 24000) -> np.ndarray:
        """调整音调 (半音)"""
        import librosa
        return librosa.effects.pitch_shift(audio, sr=sr, n_steps=semitones)
    
    @staticmethod
    def add_reverb(audio: np.ndarray, room_size: float = 0.5) -> np.ndarray:
        """添加混响效果 (简化版)"""
        # 简单的混响模拟
        delay_samples = int(room_size * 0.1 * 24000)  # 最多 100ms 延迟
        reverb_audio = audio.copy()
        
        for i in range(delay_samples, len(audio)):
            reverb_audio[i] += audio[i - delay_samples] * 0.3
        
        return reverb_audio
    
    @staticmethod
    def normalize(audio: np.ndarray) -> np.ndarray:
        """音量归一化"""
        max_val = np.abs(audio).max()
        if max_val > 0:
            return audio / max_val
        return audio
    
    @staticmethod
    def fade_in_out(audio: np.ndarray, fade_duration: float = 0.1, sr: int = 24000) -> np.ndarray:
        """淡入淡出"""
        fade_samples = int(fade_duration * sr)
        
        if len(audio) < fade_samples * 2:
            return audio
        
        # 淡入
        fade_in = np.linspace(0, 1, fade_samples)
        audio[:fade_samples] *= fade_in
        
        # 淡出
        fade_out = np.linspace(1, 0, fade_samples)
        audio[-fade_samples:] *= fade_out
        
        return audio
    
    @staticmethod
    def process(
        audio: np.ndarray,
        speed: float = 1.0,
        pitch: float = 0,
        reverb: bool = False,
        normalize: bool = True,
        fade: bool = True,
        sr: int = 24000
    ) -> np.ndarray:
        """综合处理"""
        # 调整语速
        if speed != 1.0:
            audio = AudioProcessor.adjust_speed(audio, speed)
        
        # 调整音调
        if pitch != 0:
            audio = AudioProcessor.adjust_pitch(audio, pitch, sr)
        
        # 混响
        if reverb:
            audio = AudioProcessor.add_reverb(audio)
        
        # 归一化
        if normalize:
            audio = AudioProcessor.normalize(audio)
        
        # 淡入淡出
        if fade:
            audio = AudioProcessor.fade_in_out(audio, sr=sr)
        
        return audio
    
    @staticmethod
    def process_file(
        input_path: str,
        output_path: str = None,
        speed: float = 1.0,
        pitch: float = 0,
        reverb: bool = False,
        normalize: bool = True,
        fade: bool = True
    ):
        """处理音频文件"""
        # 读取
        audio, sr = sf.read(input_path)
        
        # 处理
        audio = AudioProcessor.process(
            audio, speed, pitch, reverb, normalize, fade, sr
        )
        
        # 保存
        if output_path is None:
            output_path = input_path
        
        sf.write(output_path, audio, sr)
        return output_path
