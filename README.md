# 🎤 illli-tts

[English](#english) | [中文](#中文)

illli-tts is a powerful text-to-speech tool based on Qwen3-TTS, supporting voice cloning, voice design, and more.

---

## ✨ Features | 功能特性

- 🧠 **Qwen3-TTS** - Local offline model, 9 preset voices
- 🌐 **Edge TTS** - Microsoft online voices, more options
- 🎭 **Voice Design** - Control voice style with text descriptions
- 🔊 **Voice Cloning** - Clone voice from reference audio (requires Base model)
- 📦 **Batch Synthesis** - Batch text-to-speech
- 🎨 **Audio Processing** - Speed, pitch, reverb adjustment
- 📡 **API Service** - HTTP API interface
- 🎨 **Web UI** - Gradio visualization interface
- 📝 **History** - View and manage generation history
- 📤 **Feishu Integration** - Send audio to Feishu

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
cd illli-tts
source .venv/bin/activate
pip install -e .
```

### Basic Usage | 基本用法

```bash
# Text-to-speech
illli-tts speak "你好" -o output.wav

# With voice design
illli-tts speak "你好" --instruct "用温柔的语气" -m qwen

# Batch synthesis
illli-tts batch text.txt -o output/

# Send to Feishu
illli-tts speak "你好" --send-to-feishu

# Audio processing
illli-tts process input.wav --pitch 2 --reverb

# Start API server
illli-tts serve -p 8080

# Start Web UI
illli-tts webui -p 7860

# View history
illli-tts history
```

---

## 📋 Commands | 命令列表

| Command | Description | 说明 |
|---------|-------------|------|
| `speak` | Text-to-speech | 语音合成 |
| `batch` | Batch synthesis | 批量合成 |
| `clone` | Voice cloning | 语音克隆 |
| `preview` | Quick preview & play | 快速预览 |
| `test` | Test all voices | 测试所有音色 |
| `play` | Play audio | 播放音频 |
| `send` | Send to Feishu | 发送到飞书 |
| `convert` | Format conversion | 格式转换 |
| `resample` | Adjust sample rate | 调整采样率 |
| `process` | Audio post-processing | 后处理 |
| `merge` | Merge audio files | 合并音频 |
| `trim` | Trim audio | 裁剪音频 |
| `mix` | Mix with background music | 混合背景音乐 |
| `serve` | HTTP API server | HTTP API 服务 |
| `webui` | Web interface | Web 界面 |
| `history` | View history | 历史记录 |
| `status` | View status | 状态查看 |
| `config` | Configuration | 配置管理 |
| `voices` | List voices | 音色列表 |
| `info` | Project info | 项目信息 |
| `count` | Text statistics | 文本统计 |
| `clean` | Text cleanup | 文本清理 |

---

## 🎭 Available Voices | 可用音色

| ID | Name | Description |
|----|------|--------------|
| `female_young` | Young Female | Vivian - 明亮清脆 |
| `female_cute` | Cute Female | Serena - 温柔柔和 |
| `male_young` | Young Male | Dylan - 北京话清澈 |
| `male_mature` | Mature Male | Uncle_Fu - 成熟男性 |
| `male_sichuan` | Sichuan Male | Eric - 四川话男性 |
| `english_male` | English Male | Ryan - 英语男性 |
| `english_male_2` | English Male 2 | Aiden - 英语男性2 |
| `japanese_female` | Japanese Female | Ono_Anna - 日语女性 |
| `korean_female` | Korean Female | Sohee - 韩语女性 |

---

## ⚙️ Configuration | 配置

```bash
# View config
illli-tts config all

# Set config
illli-tts config model.cache_dir ./models
```

---

## 📁 Project Structure | 项目结构

```
illli-tts/
├── src/
│   ├── cli.py              # CLI entry
│   ├── tts.py             # Qwen3-TTS engine
│   ├── edge_tts_engine.py  # Edge TTS engine
│   ├── api.py              # HTTP API
│   ├── webui.py            # Web UI
│   ├── processor.py        # Audio processing
│   ├── history.py          # History
│   ├── sender.py           # Feishu sender
│   └── config.py           # Configuration
├── models/                  # Model files
├── README.md
└── TODO.md
```

---

## 🔗 Links | 链接

- GitHub: https://github.com/illli-studio/illli-tts
- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS

---

## 📄 License

MIT

---

# 中文

illli-tts 是一个基于 Qwen3-TTS 的强大文字转语音工具，支持语音克隆、语音设计等功能。

## 安装

```bash
cd illli-tts
source .venv/bin/activate
pip install -e .
```

## 快速开始

```bash
# 语音合成
illli-tts speak "你好" -o output.wav

# 语音设计
illli-tts speak "你好" --instruct "用温柔的语气" -m qwen

# 批量合成
illli-tts batch text.txt -o output/

# 发送到飞书
illli-tts speak "你好" --send-to-feishu

# 音频后处理
illli-tts process input.wav --pitch 2 --reverb

# 启动 API 服务
illli-tts serve -p 8080

# 启动 Web 界面
illli-tts webui -p 7860
```

## 功能列表

- Qwen3-TTS 本地离线模型
- Edge TTS 微软在线语音
- 语音设计（控制语气）
- 语音克隆
- 批量合成
- 音频后处理
- HTTP API
- Web 界面
- 历史记录
- 飞书集成

## 可用音色

- female_young (Vivian) - 年轻女性
- female_cute (Serena) - 可爱女性
- male_young (Dylan) - 年轻男性
- male_mature (Uncle_Fu) - 成熟男性
- male_sichuan (Eric) - 四川男性
- english_male (Ryan) - 英语男性
- japanese_female (Ono_Anna) - 日语女性
- korean_female (Sohee) - 韩语女性
