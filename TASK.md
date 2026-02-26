# illli-tts 项目规划

## 📌 项目概述

- **项目名称**: illli-tts
- **项目类型**: CLI 工具 (命令行文本转语音)
- **核心功能**: 基于 Qwen3-TTS 的文字转语音工具，支持语音克隆、语音设计
- **目标用户**: 工作室内部使用 + 可能开源分享
- **GitHub 仓库**: https://github.com/illli-studio/illli-tts

---

## 🎯 功能规划

### 核心功能 (MVP)

| 功能 | 描述 | 优先级 |
|------|------|--------|
| **基础 TTS** | 文字转语音，默认中文/英文 | P0 |
| **CLI 接口** | 命令行参数支持 | P0 |
| **语音发送** | 生成音频后发送到飞书 | P0 |
| **模型管理** | 自动从 ModelScope/HuggingFace 下载模型 | P0 |
| **中文支持** | 完整的中文 TTS 支持 | P0 |

### 进阶功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| **语音克隆** | 提供参考音频，克隆声音 | P1 |
| **语音设计** | 通过文字描述控制音色 | P1 |
| **语速调节** | 调整语音生成速度 | P1 |
| **多语音切换** | 支持多个预设音色 | P1 |
| **流式输出** | 实时播放生成的语音 | P2 |
| **批量合成** | 批量文本转语音 | P2 |

---

## 🏗️ 技术架构

```
illli-tts/
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI 入口
│   ├── tts.py              # TTS 核心推理
│   ├── models.py           # 模型下载管理
│   ├── voices.py           # 语音配置管理
│   └── sender.py           # 飞书音频发送
├── models/                 # 模型文件目录
│   └── qwen3-tts-1.7b-customVoice/
├── examples/               # 示例音频
├── tests/                  # 单元测试
├── pyproject.toml          # 项目配置
├── setup.py                # 安装脚本
├── README.md               # 项目文档
└── TASK.md                 # 本文件
```

### 技术选型

| 组件 | 选型 | 理由 |
|------|------|------|
| **编程语言** | Python | Qwen3-TTS 官方支持 |
| **CLI 框架** | Click / Typer | 简单易用 |
| **模型下载** | ModelScope + HuggingFace | 国内访问快 |
| **音频处理** | scipy + soundfile | 稳定可靠 |
| **发布方式** | PyPI + GitHub Release | 方便安装 |

---

## 📥 模型信息

### Qwen3-TTS-1.7B-CustomVoice

- **模型大小**: ~3.4GB
- **下载源**: ModelScope (国内) / HuggingFace (国外)
- **ModelScope ID**: qwen/Qwen3-TTS-1.7B-CustomVoice
- **HuggingFace**: Qwen/Qwen3-TTS-1.7B-CustomVoice
- **特点**:
  - 支持语音克隆
  - 支持语音设计
  - 12Hz 采样率
  - 中英日韩等多语言

### 模型文件

```
Qwen3-TTS-1.7B-CustomVoice/
├── config.json
├── configuration.json
├── model.safetensors    # 主要模型文件 (~3.4GB)
├── model.safetensors.index.json
├── tokenizer.json
└── vocab.txt
```

---

## 🔧 实现步骤

### 阶段 1: 项目初始化 (Task 1-3)

- [x] **Task 1.1**: 创建 GitHub 仓库 `illli-studio/illli-tts`
- [x] **Task 1.2**: 初始化 Python 项目结构 (pyproject.toml)
- [x] **Task 1.3**: 配置开发环境 (Python 3.10+, CUDA)

### 阶段 2: 模型集成 (Task 4-6)

- [x] **Task 2.1**: 实现模型下载器 (支持 ModelScope/HuggingFace)
- [x] **Task 2.2**: 实现模型加载和推理封装
- [ ] **Task 2.3**: 测试基础 TTS 功能 (⚠️ 网络问题，模型下载失败)

> ⚠️ **网络问题**: 当前无法访问 ModelScope/HuggingFace，需要代理或手动下载模型

### 阶段 3: CLI 开发 (Task 7-10)

- [ ] **Task 3.1**: 实现 CLI 框架 (Click/Typer)
- [ ] **Task 3.2**: 添加基础 TTS 命令
- [ ] **Task 3.3**: 添加语音克隆功能
- [ ] **Task 3.4**: 添加语音设计功能

### 阶段 4: 集成飞书 (Task 11-12)

- [ ] **Task 4.1**: 集成飞书消息发送功能
- [ ] **Task 4.2**: 实现 "你说 → 我发语音" 流程

### 阶段 5: 优化与发布 (Task 13-15)

- [ ] **Task 5.1**: 添加配置管理 (模型路径、默认参数)
- [ ] **Task 5.2**: 优化推理速度
- [ ] **Task 5.3**: 编写 README 和使用文档
- [ ] **Task 5.4**: 发布到 PyPI (可选)

---

## 📝 命令行接口设计

```bash
# 基础用法
illli-tts "你好，这是一个测试"

# 指定输出文件
illli-tts "你好" -o output.wav

# 使用指定音色
illli-tts "你好" -v female_cute

# 语音克隆 (需要参考音频)
illli-tts "你好" --ref-audio reference.wav -o output.wav

# 语音设计 (文字描述)
illli-tts "你好" --voice-description "年轻的女性声音，温柔甜美"

# 调节语速
illli-tts "你好" --speed 1.2

# 发送到飞书
illli-tts "你好" --send-to-feishu

# 查看帮助
illli-tts --help
```

---

## ⚙️ 配置说明

### 默认配置 (config.yaml)

```yaml
model:
  name: "Qwen3-TTS-1.7B-CustomVoice"
  download_source: "modelscope"  # modelscope / huggingface
  cache_dir: "./models"

tts:
  default_language: "zh"
  default_speed: 1.0
  default_voice: "female_young"

voices:
  female_young:
    name: "年轻女性"
    description: "温柔甜美的女声"
  male_young:
    name: "年轻男性"
    description: "清澈干净的男声"
  custom:
    name: "自定义"
    description: "需要提供参考音频"

feishu:
  enabled: true
  default_target: "self"  # 发送给自己
```

---

## 🔄 工作流程

### 场景 1: 你说话 → 我发语音

```
用户 (飞书) → 发送文字 → OpenClaw 接收 
→ 调用 illli-tts 生成语音 
→ 发送语音到飞书 → 用户收到
```

### 场景 2: 命令行使用

```bash
# 开发调试
cd illli-tts
python -m src.cli "你好世界" -o test.wav

# 生产使用
illli-tts "今天天气真好" --send-to-feishu
```

---

## 📦 依赖清单

```toml
# pyproject.toml 主要依赖

[project]
name = "illli-tts"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "click>=8.1.0",       # CLI 框架
    "torch>=2.0",         # 深度学习框架
    "transformers>=4.30", # HuggingFace transformers
    "modelscope>=1.9.0",  # ModelScope 模型下载
    "soundfile>=0.12.0",  # 音频读写
    "scipy>=1.11.0",      # 音频处理
    "numpy>=1.24",        # 数值计算
    "pyyaml>=6.0",        # 配置管理
    "httpx>=0.24",        # HTTP 请求
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1.0",
]
```

---

## ⚠️ 注意事项

1. **GPU 要求**: 建议 6GB+ 显存，CPU 模式会很慢
2. **首次运行**: 需要下载 ~3.4GB 模型，请确保网络通畅
3. **ModelScope**: 国内访问速度快，首次使用需要登录 (可选)
4. **音频格式**: 默认输出 WAV，可转 MP3

---

## 📅 预计工作量

| 阶段 | 任务数 | 预计时间 |
|------|--------|---------|
| 阶段 1 | 3 | 30 min |
| 阶段 2 | 3 | 2 h |
| 阶段 3 | 4 | 3 h |
| 阶段 4 | 2 | 1 h |
| 阶段 5 | 4 | 2 h |
| **总计** | **16** | **~8.5 h** |

---

*Created by 小灵 🐱*
*Date: 2026-02-26*
