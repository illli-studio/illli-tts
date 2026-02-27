"""API 服务模块"""

import os
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from .tts import TTSEngine
from .edge_tts_engine import EdgeTTSEngine

app = FastAPI(title="illli-tts API", version="0.2.0")

# 全局引擎
_qwen_engine = None
_edge_engine = None


def get_qwen_engine():
    global _qwen_engine
    if _qwen_engine is None:
        _qwen_engine = TTSEngine()
    return _qwen_engine


def get_edge_engine():
    global _edge_engine
    if _edge_engine is None:
        _edge_engine = EdgeTTSEngine()
    return _edge_engine


class TTSRequest(BaseModel):
    text: str
    voice: str = "female_young"
    speed: float = 1.0
    model: str = "qwen"  # qwen, edge, say
    instruct: Optional[str] = None


class TTSResponse(BaseModel):
    success: bool
    audio_path: Optional[str] = None
    message: Optional[str] = None


@app.get("/")
def root():
    return {"name": "illli-tts API", "version": "0.2.0"}


@app.get("/voices")
def list_voices():
    """获取可用音色列表"""
    return {
        "voices": [
            {"id": "female_young", "name": "年轻女性", "speaker": "Vivian"},
            {"id": "female_cute", "name": "可爱女性", "speaker": "Serena"},
            {"id": "male_young", "name": "年轻男性", "speaker": "Dylan"},
            {"id": "male_mature", "name": "成熟男性", "speaker": "Uncle_Fu"},
            {"id": "male_sichuan", "name": "四川男性", "speaker": "Eric"},
            {"id": "english_male", "name": "英语男性", "speaker": "Ryan"},
            {"id": "english_male_2", "name": "英语男性2", "speaker": "Aiden"},
            {"id": "japanese_female", "name": "日语女性", "speaker": "Ono_Anna"},
            {"id": "korean_female", "name": "韩语女性", "speaker": "Sohee"},
        ]
    }


@app.post("/tts", response_model=TTSResponse)
def tts(request: TTSRequest):
    """文字转语音"""
    import tempfile
    import uuid
    
    try:
        # 生成输出路径
        output_path = f"/tmp/tts_{uuid.uuid4().hex}.wav"
        
        if request.model == "qwen":
            engine = get_qwen_engine()
            audio = engine.speak(
                text=request.text,
                voice=request.voice,
                speed=request.speed,
                instruct=request.instruct,
            )
            engine.save(audio, output_path)
            
        elif request.model == "edge":
            engine = get_edge_engine()
            engine.speak(
                text=request.text,
                voice=request.voice,
                speed=request.speed,
                output_file=output_path,
            )
            
        elif request.model == "say":
            engine = get_qwen_engine()
            engine.speak_fallback(request.text, request.voice, output_path)
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown model: {request.model}")
        
        return TTSResponse(success=True, audio_path=output_path)
        
    except Exception as e:
        return TTSResponse(success=False, message=str(e))


@app.post("/tts/stream")
def tts_stream(request: TTSRequest):
    """流式语音合成（返回 base64）"""
    import base64
    import tempfile
    
    try:
        output_path = f"/tmp/tts_{uuid.uuid4().hex}.wav"
        
        if request.model == "qwen":
            engine = get_qwen_engine()
            audio = engine.speak(
                text=request.text,
                voice=request.voice,
                speed=request.speed,
                instruct=request.instruct,
            )
            engine.save(audio, output_path)
            
        elif request.model == "edge":
            engine = get_edge_engine()
            engine.speak(
                text=request.text,
                voice=request.voice,
                speed=request.speed,
                output_file=output_path,
            )
        
        # 读取并转为 base64
        with open(output_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode()
        
        # 清理临时文件
        Path(output_path).unlink(missing_ok=True)
        
        return {
            "success": True,
            "audio": audio_base64,
            "format": "wav"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 启动服务
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
