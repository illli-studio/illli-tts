"""飞书音频发送模块"""

import os
import base64
from pathlib import Path
from typing import Optional

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class FeishuSender:
    """飞书音频发送器"""
    
    # 飞书开放平台 API
    API_BASE = "https://open.feishu.cn/open-apis"
    
    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        self.app_id = app_id or os.environ.get("FEISHU_APP_ID")
        self.app_secret = app_secret or os.environ.get("FEISHU_APP_SECRET")
        self.access_token = None
    
    def _get_access_token(self) -> str:
        """获取 access_token"""
        if not HAS_HTTPX:
            raise ImportError("httpx is required. Install with: pip install httpx")
        
        if self.access_token:
            return self.access_token
        
        url = f"{self.API_BASE}/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = httpx.post(url, json=data, timeout=30)
        result = response.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"获取 access_token 失败: {result}")
        
        self.access_token = result["tenant_access_token"]
        return self.access_token
    
    def _upload_audio(self, audio_path: str) -> str:
        """上传音频文件到飞书"""
        token = self._get_access_token()
        
        url = f"{self.API_BASE}/im/v1/files"
        
        # 读取音频文件
        with open(audio_path, "rb") as f:
            audio_data = f.read()
        
        # Base64 编码
        audio_base64 = base64.b64encode(audio_data).decode()
        
        # 获取文件扩展名
        ext = Path(audio_path).suffix.lstrip(".")
        file_name = Path(audio_path).name
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        data = {
            "file_type": "mp3",
            "file_name": file_name,
            "file_size": len(audio_data),
            "audio_type": ext
        }
        
        # 注意: 飞书文件上传需要使用 multipart/form-data
        # 这里简化处理，实际需要使用 proper multipart upload
        files = {
            "file": (file_name, audio_data, f"audio/{ext}")
        }
        
        response = httpx.post(url, headers=headers, data=data, files=files, timeout=60)
        result = response.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"上传文件失败: {result}")
        
        return result["data"]["file_key"]
    
    def send_audio(
        self,
        audio_path: str,
        text: str = None,
        receive_id: Optional[str] = None,
        receive_id_type: str = "open_id"
    ):
        """发送音频消息"""
        if not HAS_HTTPX:
            raise ImportError("httpx is required")
        
        # 上传音频
        file_key = self._upload_audio(audio_path)
        
        # 发送消息
        token = self._get_access_token()
        
        url = f"{self.API_BASE}/im/v1/messages"
        params = {
            "receive_id_type": receive_id_type
        }
        
        # 构建消息内容
        content = {
            "file_key": file_key
        }
        
        if text:
            # 添加文字说明
            content["text"] = text
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "receive_id": receive_id or "self",
            "msg_type": "audio",
            "content": str(content)
        }
        
        response = httpx.post(url, headers=headers, params=params, json=data, timeout=30)
        result = response.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"发送消息失败: {result}")
        
        return result
    
    def send_text(self, text: str, receive_id: Optional[str] = None):
        """发送文字消息"""
        if not HAS_HTTPX:
            raise ImportError("httpx is required")
        
        token = self._get_access_token()
        
        url = f"{self.API_BASE}/im/v1/messages"
        params = {
            "receive_id_type": "open_id"
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "receive_id": receive_id or "self",
            "msg_type": "text",
            "content": {"text": text}
        }
        
        response = httpx.post(url, headers=headers, params=params, json=data, timeout=30)
        result = response.json()
        
        if result.get("code") != 0:
            raise RuntimeError(f"发送消息失败: {result}")
        
        return result
