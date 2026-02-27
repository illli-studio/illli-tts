# 🎤 illli-tts

基于 Qwen3-TTS 的文字转语音工具，支持语音克隆、语音设计等功能。

## 功能特性

- 🧠 **Qwen3-TTS** - 本地离线模型，支持 9 种预设音色
- 🌐 **Edge TTS** - 微软在线语音，更多音色选择
- 🎭 **语音设计** - 通过文字描述控制音色和语气
- 🔊 **语音克隆** - 使用参考音频克隆声音 (需要 Base 模型)
- 📦 **批量合成** - 批量文本转语音
- 🎨 **音频后处理** - 调整语速、音调、混响等
- 📡 **API 服务** - HTTP API 接口
- 🎨 **Web 界面** - Gradio 可视化界面
- 📝 **历史记录** - 查看和管理生成历史

## 安装

```bash
cd illli-tts
source .venv/bin/activate
pip install -e .
```

## 快速开始

### 命令行

```bash
# 基本语音合成
illli-tts speak "你好" -o output.wav

# 使用语音设计
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

# 查看历史
illli-tts history
```

### API

```bash
# 启动服务
illli-tts serve -p 8080

# 调用
curl -X POST http://localhost:8080/tts \
  -H "Content-Type: application/json" \
  -d '{"text": "你好", "voice": "female_young", "model": "qwen"}'
```

## 可用音色

| ID | 名称 | 描述 |
|---|---|---|
| female_young | 年轻女性 | Vivian - 明亮清脆 |
| female_cute | 可爱女性 | Serena - 温柔柔和 |
| male_young | 年轻男性 | Dylan - 北京话清澈 |
| male_mature | 成熟男性 | Uncle_Fu - 低沉成熟 |
| male_sichuan | 四川男性 | Eric - 充满活力 |
| english_male | 英语男性 | Ryan - 节奏感强 |
| english_male_2 | 英语男性2 | Aiden - 阳光清晰 |
| japanese_female | 日语女性 | Ono_Anna - 轻快活泼 |
| korean_female | 韩语女性 | Sohee - 温暖情感 |

## 配置

```bash
# 查看配置
illli-tts config all

# 设置配置
illli-tts config model.cache_dir ./models
```

## 项目结构

```
illli-tts/
├── src/
│   ├── cli.py          # CLI 入口
│   ├── tts.py          # Qwen3-TTS 引擎
│   ├── edge_tts_engine.py  # Edge TTS 引擎
│   ├── api.py          # HTTP API
│   ├── webui.py        # Web 界面
│   ├── processor.py     # 音频后处理
│   ├── history.py       # 历史记录
│   ├── sender.py        # 飞书发送
│   └── config.py        # 配置管理
├── models/              # 模型文件
└── README.md
```

## License

MIT
