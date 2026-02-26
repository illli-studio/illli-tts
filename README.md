# 🎙️ illli-tts

基于 Qwen3-TTS 的 CLI 文字转语音工具 | 支持 Edge TTS 和语音克隆

## ✨ 特性

- 🎵 **高质量 TTS** - 基于 Qwen3-TTS 模型
- 🔊 **多引擎支持** - Edge TTS / macOS say / Qwen3-TTS
- 🎭 **多种音色** - 年轻女性、成熟男性、童声等
- 🌍 **多语言** - 中文、英文、日语、韩语等
- 📤 **飞书集成** - 一键发送语音到飞书
- 🍎 **Mac 原生支持** - 完美支持 Apple Silicon (M1/M2/M3/M4)

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/illli-studio/illli-tts.git
cd illli-tts

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e .
```

### 使用方法

```bash
# 基础用法 (默认 Edge TTS)
illli-tts speak "你好，世界"

# 指定音色
illli-tts speak "你好" -v male_young
illli-tts speak "你好" -v female_mature

# 调整语速 (0.5-2.0)
illli-tts speak "你好" -s 1.5

# 指定输出文件
illli-tts speak "你好" -o my_voice.wav

# 使用不同引擎
illli-tts speak "你好" -m edge   # 微软 Edge (默认，推荐)
illli-tts speak "你好" -m say    # macOS say
illli-tts speak "你好" -m qwen   # Qwen3-TTS (需要下载模型)

# 生成并发送到飞书
illli-tts send "你好"

# 查看可用音色
illli-tts voices

# 查看状态
illli-tts status
```

## 🎭 可用音色

| 音色 ID | 名称 | 描述 |
|---------|------|------|
| female_young | 年轻女性 | 温柔甜美的女声 |
| male_young | 年轻男性 | 清澈干净的男声 |
| female_mature | 成熟女性 | 成熟稳重的女声 |
| male_mature | 成熟男性 | 成熟稳重的男声 |
| female_child | 小女孩 |可爱的小女孩声音 |
| male_child | 小男孩 | 活泼的小男孩声音 |

## 🧠 Qwen3-TTS 模型下载

由于网络原因，可能需要手动下载模型：

```bash
# 方法 1: 配置代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
illli-tts download

# 方法 2: 手动下载
# 1. 访问: https://modelscope.cn/models/qwen/Qwen3-TTS-1.7B
# 2. 下载模型文件
# 3. 放到: ./models/Qwen3-TTS-1.7B/
```

## 🔧 配置

配置文件: `~/.illli-tts/config.yaml`

```yaml
model:
  name: "Qwen3-TTS-1.7B"
  download_source: "modelscope"
  cache_dir: "./models"

tts:
  default_language: "zh"
  default_speed: 1.0
  default_voice: "female_young"

feishu:
  enabled: false
```

## 📋 命令列表

| 命令 | 描述 |
|------|------|
| `speak` | 文字转语音 |
| `send` | 生成语音并发送到飞书 |
| `download` | 下载 Qwen3-TTS 模型 |
| `voices` | 列出所有可用音色 |
| `status` | 查看状态 |

## 🐳 Docker 部署

```bash
docker build -t illli-tts .
docker run -it illli-tts speak "你好"
```

## 📦 依赖

- Python 3.10+
- PyTorch 2.0+ (用于 Qwen3-TTS)
- edge-tts (用于 Edge TTS)
- click (CLI 框架)

## 📄 许可证

MIT License

## 👤 作者

illli Studio

---

> 💡 **提示**: 使用 `-m edge` 可以获得最好的中文语音效果，无需下载大模型！
