# illli-tts

基于 Qwen3-TTS 的 CLI 文字转语音工具

## 功能特性

- 🎵 高质量文字转语音 (TTS)
- 🎭 多种内置音色 (Edge TTS)
- 🔊 语音克隆支持 (Qwen3-TTS, 需要下载模型)
- 🎨 语音设计 (文字描述控制音色, Qwen3-TTS)
- 📤 支持发送到飞书

## 安装

```bash
# 克隆项目
git clone https://github.com/illli-studio/illli-tts.git
cd illli-tts

# 创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv pip install -e .
```

## 快速开始

### 1. 基础用法 (Edge TTS - 推荐)

```bash
# 基础 TTS (不需要下载模型)
illli-tts speak "你好，世界"

# 指定音色
illli-tts speak "你好" -v male_young

# 调整语速
illli-tts speak "你好" -s 1.5
```

### 2. 使用 Qwen3-TTS 模型 (需要下载)

```bash
# 先下载模型
illli-tts download

# 使用模型
illli-tts speak "你好" -m qwen

# 语音克隆 (需要参考音频)
illli-tts speak "你好" --ref-audio my_voice.wav

# 语音设计
illli-tts speak "你好" --voice-desc "年轻的女性声音，温柔甜美"
```

## 可用音色

### Edge TTS (在线)
- `female_young` - 年轻女性 (晓晓)
- `male_young` - 年轻男性 (云希)
- `female_mature` - 成熟女性 (晓悠)
- `male_mature` - 成熟男性 (云扬)

### Qwen3-TTS (需要模型)
- `female_young` - 年轻女性
- `male_young` - 年轻男性
- 支持自定义语音克隆

## 下载模型

由于网络原因，可能需要手动下载模型：

```bash
# 方法 1: 配置代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
illli-tts download

# 方法 2: 手动下载
# 1. 访问 https://modelscope.cn/models/qwen/Qwen3-TTS-1.7B
# 2. 登录下载模型文件
# 3. 放到 ./models/Qwen3-TTS-1.7B/ 目录

# 方法 3: 使用 HuggingFace
# 1. 访问 https://huggingface.co/Qwen/Qwen3-TTS-1.7B
# 2. 使用代理下载
# 3. 放到 ./models/Qwen3-TTS-1.7B/ 目录
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
  name: "Qwen3-TTS-1.7B"
  download_source: "modelscope"
  cache_dir: "./models"

tts:
  default_language: "zh"
  default_speed: 1.0
  default_voice: "female_young"
```

## 环境要求

- Python 3.10+
- Edge TTS: 无需 GPU，直接使用
- Qwen3-TTS: 6GB+ GPU 显存 (推荐)
- 20GB+ 磁盘空间 (模型约 3.4GB)

## 许可证

MIT License
