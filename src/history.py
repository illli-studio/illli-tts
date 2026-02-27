"""历史记录模块"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional


class HistoryManager:
    """历史记录管理"""
    
    def __init__(self, history_file: str = None):
        if history_file is None:
            history_file = os.path.expanduser("~/.illli-tts/history.json")
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        self.history = self._load()
    
    def _load(self) -> List[dict]:
        if self.history_file.exists():
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add(self, text: str, voice: str, model: str, audio_path: str, instruct: str = None):
        """添加记录"""
        record = {
            "id": len(self.history) + 1,
            "text": text,
            "voice": voice,
            "model": model,
            "instruct": instruct,
            "audio_path": audio_path,
            "timestamp": datetime.now().isoformat()
        }
        self.history.insert(0, record)  # 最近的在前面
        
        # 只保留最近 100 条
        if len(self.history) > 100:
            self.history = self.history[:100]
        
        self._save()
        return record
    
    def list(self, limit: int = 10) -> List[dict]:
        """列出历史记录"""
        return self.history[:limit]
    
    def get(self, record_id: int) -> Optional[dict]:
        """获取单条记录"""
        for r in self.history:
            if r["id"] == record_id:
                return r
        return None
    
    def clear(self):
        """清空历史"""
        self.history = []
        self._save()
    
    def delete(self, record_id: int):
        """删除单条记录"""
        self.history = [r for r in self.history if r["id"] != record_id]
        self._save()


# 全局实例
_history = None

def get_history():
    global _history
    if _history is None:
        _history = HistoryManager()
    return _history
