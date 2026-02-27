# 🎤 illli-tts

基于 Qwen3-TTS 的文字转语音工具

## 安装

```bash
cd illli-tts
source .venv/bin/activate
```

## 命令列表

| 命令 | 说明 |
|------|------|
| **speak** | 语音合成 |
| **batch** | 批量合成 |
| **clone** | 语音克隆 |
| **preview** | 快速预览+播放 |
| **test** | 测试所有音色 |
| **play** | 播放音频 |
| **send** | 发送到飞书 |
| **convert** | 格式转换 |
| **merge** | 合并音频 |
| **trim** | 裁剪音频 |
| **mix** | 混合背景音乐 |
| **process** | 后处理 |
| **resample** | 调整采样率 |
| **serve** | HTTP API |
| **webui** | Web 界面 |
| **history** | 历史记录 |
| **status** | 状态查看 |
| **config** | 配置管理 |
| **voices** | 音色列表 |
| **info** | 项目信息 |
| **count** | 文本统计 |
| **clean** | 文本清理 |

## 示例

```bash
# 基本合成
illli-tts speak "你好" -o test.wav

# 带后处理
illli-tts speak "你好" --pitch 2 --reverb

# 批量合成
illli-tts batch text.txt -o output/

# 预览
illli-tts preview "你好"

# 格式转换
illli-tts convert input.wav mp3

# 统计
illli-tts count "你好 world"
```
