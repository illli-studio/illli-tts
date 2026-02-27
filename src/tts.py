"""TTS 推理引擎模块 - Qwen3-TTS"""

import torch
import numpy as np
from pathlib import Path
from typing import Optional, Union, List
import soundfile as sf

from .config import Config


# 支持的音色列表 (CustomVoice 模型)
SUPPORTED_SPEAKERS = [
    "Vivian",      # 中文年轻女性，明亮略带尖锐
    "Serena",      # 中文年轻女性，温暖柔和
    "Uncle_Fu",    # 中年男性，低沉成熟
    "Dylan",       # 北京话男性，年轻清澈
    "Eric",       # 四川话男性，充满活力
    "Ryan",        # 英语男性，节奏感强
    "Aiden",       # 英语男性，阳光清晰
    "Ono_Anna",   # 日语女性，轻快活泼
    "Sohee",       # 韩语女性，温暖富有情感
]

# 音色映射到内部名称
SPEAKER_MAP = {
    "female_young": "Vivian",
    "female_cute": "Serena",
    "male_young": "Dylan",
    "male_mature": "Uncle_Fu",
    "male_sichuan": "Eric",
    "english_male": "Ryan",
    "english_male_2": "Aiden",
    "japanese_female": "Ono_Anna",
    "korean_female": "Sohee",
}


class TTSEngine:
    """Qwen3-TTS 推理引擎"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.model = None
        self.model_path = None
        self.sampling_rate = 24000
        
        # 确定设备
        if torch.cuda.is_available():
            self.device = "cuda"
            print("💡 使用 NVIDIA GPU 加速")
        elif torch.backends.mps.is_available():
            self.device = "mps"
            print("💡 使用 Apple MPS (Metal) 加速")
        else:
            self.device = "cpu"
            print("💡 使用 CPU")
    
    def _load_model(self):
        """加载模型"""
        if self.model is not None:
            return
        
        model_path = self._find_model_path()
        
        if model_path is None:
            raise RuntimeError(
                f"模型未找到！\n\n"
                "请确保模型已下载到:\n"
                "  - ./models/Qwen3-TTS-12Hz-1.7B-CustomVoice/\n"
            )
        
        print(f"🔄 加载 Qwen3-TTS 模型 from {model_path}...")
        
        try:
            from qwen_tts import Qwen3TTSModel
            
            if self.device in ["cuda", "mps"]:
                dtype = torch.float16
            else:
                dtype = torch.float32
            
            self.model = Qwen3TTSModel.from_pretrained(
                str(model_path),
                device_map=self.device,
                dtype=dtype,
            )
            
            print(f"✅ 模型加载成功！使用设备: {self.device}")
            
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            raise
    
    def _find_model_path(self):
        """查找本地模型路径"""
        possible_paths = [
            Path("./models/Qwen3-TTS-12Hz-1.7B-CustomVoice"),
            Path("./models/Qwen3-TTS-1.7B-CustomVoice"),
            Path("/Users/elham/.openclaw/workspace/illli-tts/models/Qwen3-TTS-12Hz-1.7B-CustomVoice"),
        ]
        
        for path in possible_paths:
            if path.exists() and (path / "model.safetensors").exists():
                self.model_path = path
                return path
        return None
    
    def get_supported_speakers(self) -> List[str]:
        return SUPPORTED_SPEAKERS.copy()
    
    def speak(
        self,
        text: str,
        voice: str = "female_young",
        speed: float = 1.0,
        ref_audio: Optional[str] = None,
        voice_desc: Optional[str] = None,
        instruct: Optional[str] = None,
    ) -> np.ndarray:
        """生成语音"""
        self._load_model()
        
        speaker = SPEAKER_MAP.get(voice, voice)
        if speaker not in SUPPORTED_SPEAKERS:
            speaker = "Vivian"
        
        language = self._detect_language(text)
        
        print(f"🎵 生成语音: {text[:30]}...")
        print(f"   音色: {speaker}")
        if instruct:
            print(f"   指令: {instruct}")
        if ref_audio:
            print(f"   参考音频: {ref_audio}")
        
        # 如果有 instruct，使用 instruct 控制
        # 如果有 ref_audio，使用语音克隆
        wavs, sr = self.model.generate_custom_voice(
            text=text,
            language=language,
            speaker=speaker,
            instruct=instruct,
        )
        
        audio = wavs[0]
        self.sampling_rate = sr
        
        return audio
    
    def speak_clone(self, text: str, ref_audio: str, speed: float = 1.0) -> np.ndarray:
        """语音克隆 - 使用参考音频"""
        self._load_model()
        
        language = self._detect_language(text)
        
        print(f"🎵 语音克隆: {text[:30]}...")
        print(f"   参考音频: {ref_audio}")
        
        # 加载参考音频
        import soundfile as sf
        ref_wav, ref_sr = sf.read(ref_audio)
        
        # 重采样如果需要
        if ref_sr != 24000:
            import librosa
            ref_wav = librosa.resample(ref_wav, orig_sr=ref_sr, target_sr=24000)
        
        wavs, sr = self.model.generate_voice_clone(
            text=text,
            language=language,
            audio_prompt=ref_wav,
        )
        
        audio = wavs[0]
        self.sampling_rate = sr
        
        return audio
    
    def _detect_language(self, text: str) -> str:
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)
        if has_chinese:
            return "Chinese"
        has_japanese = any('\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff' for c in text)
        if has_japanese:
            return "Japanese"
        has_korean = any('\uac00' <= c <= '\ud7af' for c in text)
        if has_korean:
            return "Korean"
        return "English"
    
    def save(self, audio: np.ndarray, path: Union[str, Path], sr: int = None):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        sr = sr or self.sampling_rate
        
        if isinstance(audio, torch.Tensor):
            audio = audio.cpu().numpy()
        
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        if audio.max() > 1.0:
            audio = audio / np.abs(audio).max()
        
        sf.write(str(path), audio, sr)
        print(f"💾 已保存到: {path}")
    
    def speak_fallback(self, text: str, voice: str = "female_young", output_path: str = "/tmp/illli-tts-fallback.wav") -> str:
        """使用 macOS say 命令作为备选"""
        import subprocess
        
        voice_map = {
            "female_young": "Samantha",
            "male_young": "Daniel", 
            "female_mature": "Victoria",
            "male_mature": "James",
        }
        
        macos_voice = voice_map.get(voice, "Samantha")
        
        aiff_path = "/tmp/illli-tts-temp.aiff"
        subprocess.run(["say", "-v", macos_voice, "-o", aiff_path, text], check=True)
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", aiff_path, output_path], check=True)
        Path(aiff_path).unlink(missing_ok=True)
        
        return output_path
