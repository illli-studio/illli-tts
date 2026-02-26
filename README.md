# illli-tts

基于 Qwen3-TTS 的 CLI 文字转语音工具

## 功能特性

- 🎵 高质量文字转语音 (TTS)
- 🎭 多种内置音色
- 🔊 语音克隆支持 (需要参考音频)
- 🎨 语音设计 (文字描述控制音色)
- 📤 支持发送到飞书

## 安装

```bash
# 克隆项目
git clone https://github.com/illli-studio/illli-tts.git
cd illli-tts

# 安装依赖
pip install -e .
```

## 快速开始

### 1. 下载模型

```bash
illli-tts download
```

### 2. 基本用法

```bash
# 基础 TTS
illli-tts speak "你好，世界"

# 指定音色
illli-tts speak "你好" -v male_young

# 调整语速
illli-tts speak "你好" -s 1.5

# 语音克隆
illli-tts speak "你好" --ref-audio my_voice.wav

# 语音设计
illli-tts speak "你好" --voice-desc "年轻的女性声音，温柔甜美"
```

### 3. 发送到飞书

```bash
illli-tts send "你好" -v female_young
```

## 命令列表

| 命令 | 描述 |
|------|------|
| `speak` | 将文字转为语音 |
| `send` | 生成语音并发送到飞书 |
| `download` | 下载模型 |
| `voices` | 列出所有可用音色 |
| `status` | 查看模型状态 |

## 配置

配置文件位于: `~/.illli-tts/config.yaml`

```yaml
model:
  name: "Qwen3-TTS-1.7B-CustomVoice"
  download_source: "modelscope"
  cache_dir: "./models"

tts:
  default_language: "zh"
  default_speed: 1.0
  default_voice: "female_young"
```

## 环境要求

- Python 3.10+
- PyTorch 2.0+
- 6GB+ GPU 显存 (推荐)
- 20GB+ 磁盘空间 (模型约 3.4GB)

## 许可证

MIT License
