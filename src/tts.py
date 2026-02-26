"""TTS 推理引擎模块"""

import torch
import numpy as np
from pathlib import Path
from typing import Optional, Union
import soundfile as sf

from .config import Config
from .models import ModelManager


class TTSEngine:
    """Qwen3-TTS 推理引擎"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.model_manager = ModelManager(self.config)
        self.model = None
        self.processor = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def _load_model(self):
        """加载模型"""
        if self.model is not None:
            return
        
        model_path = self.model_manager.get_model_path()
        if model_path is None:
            raise RuntimeError(
                "模型未下载！请先运行 'illli-tts download' 下载模型，"
                "或者设置 ModelScope/HuggingFace API key"
            )
        
        print(f"🔄 加载模型 from {model_path}...")
        
        try:
            from transformers import AutoProcessor, AutoModelForCausalLM
            
            self.processor = AutoProcessor.from_pretrained(
                str(model_path),
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.model.to(self.device)
            self.model.eval()
            
            print(f"✅ 模型加载成功！使用设备: {self.device}")
            
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            raise
    
    def speak(
        self,
        text: str,
        voice: str = "female_young",
        speed: float = 1.0,
        ref_audio: Optional[str] = None,
        voice_desc: Optional[str] = None
    ) -> np.ndarray:
        """生成语音"""
        self._load_model()
        
        # 构建输入
        inputs = self.processor(
            text=text,
            return_tensors="pt",
            function=voice,
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # 生成
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                do_sample=True,
                temperature=0.8,
            )
        
        # 解码
        audio = self.processor.decode(
            output[0],
            audio_prompt=ref_audio if ref_audio else None,
            voice_description=voice_desc,
        )
        
        return audio
    
    def save(self, audio: np.ndarray, path: Union[str, Path]):
        """保存音频到文件"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # 转换为 float32 并归一化
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        
        # 确保范围在 [-1, 1]
        if audio.max() > 1.0:
            audio = audio / 32768.0
        
        sf.write(str(path), audio, 24000)  # Qwen3-TTS 默认 24kHz
    
    def stream(self, text: str, voice: str = "female_young"):
        """流式播放 (需要实现)"""
        raise NotImplementedError("流式播放功能待实现")
