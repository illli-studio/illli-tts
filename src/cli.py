"""CLI 入口 - illli-tts 命令行工具"""

import sys
import os
import json
import click
from pathlib import Path
from datetime import datetime

from .tts import TTSEngine
from .edge_tts_engine import EdgeTTSEngine
from .models import ModelManager
from .voices import VoiceManager
from .sender import FeishuSender
from .config import Config
from .history import get_history
from .processor import AudioProcessor


@click.group()
@click.version_option(version="0.2.0")
def cli():
    """illli-tts: 基于 Qwen3-TTS 的文字转语音工具"""
    pass


@cli.command()
@click.argument("text", required=False)
@click.option("-f", "--file", "input_file", type=click.Path(exists=True), help="从文件读取文本 (支持 .txt, .json)")
@click.option("-o", "--output", "output_file", help="输出文件路径", default="output.wav")
@click.option("-v", "--voice", "voice", help="音色", default="female_young")
@click.option("-s", "--speed", "speed", help="语速 (0.5-2.0)", default=1.0, type=float)
@click.option("-m", "--model", "model_type", help="模型: qwen/edge/say", default="qwen")
@click.option("--instruct", "instruct", help="语音指令 (语音设计)", default=None)
@click.option("--send-to-feishu", "send_to_feishu", is_flag=True, help="发送到飞书")
@click.option("--format", "audio_format", help="输出格式: wav/mp3", default="wav")
@click.option("--pitch", "pitch", help="音调 (-12 到 12)", default=0, type=int)
@click.option("--reverb", "reverb", is_flag=True, help="添加混响")
@click.option("-q", "--quiet", "quiet", is_flag=True, help="安静模式")
def speak(text, input_file, output_file, voice, speed, model_type, instruct, send_to_feishu, audio_format, pitch, reverb, quiet):
    """将文字转为语音"""
    
    # 读取文本
    if input_file:
        ext = Path(input_file).suffix.lower()
        if ext == ".json":
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                text = data.get("text", data.get("content", ""))
        else:
            with open(input_file, "r", encoding="utf-8") as f:
                text = f.read().strip()
    elif not text:
        click.echo("Error: 请提供文字或使用 -f/--file 指定文件")
        return
    
    if not quiet:
        click.echo(f"📝 {text[:60]}{'...' if len(text) > 60 else ''}")
    
    output_path = None
    start_time = datetime.now()
    
    # 生成
    if model_type == "edge":
        if not quiet:
            click.echo(f"🎵 Edge TTS | 音色: {voice}")
        engine = EdgeTTSEngine()
        tmp_file = output_file if output_file.endswith(".mp3") else output_file + ".mp3"
        output_path = engine.speak(text, voice, speed, output_file=tmp_file)
        if output_path.endswith(".mp3"):
            wav_path = output_path.replace(".mp3", ".wav")
            import subprocess
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", output_path, wav_path], check=True, capture_output=True)
            output_path = wav_path
        
    elif model_type == "say":
        if not quiet:
            click.echo(f"🎤 macOS say | 音色: {voice}")
        engine = TTSEngine()
        output_path = engine.speak_fallback(text, voice, output_file)
        
    elif model_type == "qwen":
        if not quiet:
            click.echo(f"🧠 Qwen3-TTS | 音色: {voice}")
            if instruct:
                click.echo(f"   指令: {instruct}")
        engine = TTSEngine()
        audio = engine.speak(text=text, voice=voice, speed=speed, instruct=instruct)
        engine.save(audio, output_file)
        output_path = output_file
    else:
        click.echo(f"❌ 未知模型: {model_type}")
        return
    
    # 后处理
    if pitch != 0 or reverb:
        processed = output_path.replace(".wav", "_processed.wav")
        AudioProcessor.process_file(output_path, processed, pitch=pitch, reverb=reverb)
        output_path = processed
    
    # 格式转换
    if audio_format == "mp3" and not output_path.endswith(".mp3"):
        mp3_path = output_path.replace(".wav", ".mp3")
        import subprocess
        subprocess.run(["afconvert", "-f", "mp4f", "-d", "aac", output_path, mp3_path], check=True, capture_output=True)
        output_path = mp3_path
    
    # 统计
    elapsed = (datetime.now() - start_time).total_seconds()
    file_size = os.path.getsize(output_path) / 1024  # KB
    
    if not quiet:
        click.echo(f"✅ 已保存: {output_path} ({file_size:.1f}KB, {elapsed:.1f}s)")
    else:
        click.echo(output_path)
    
    # 发送到飞书
    if send_to_feishu:
        try:
            sender = FeishuSender()
            sender.send_audio(output_path, message=f"🎵 {text[:30]}...")
            if not quiet:
                click.echo("📤 已发送到飞书")
        except Exception as e:
            click.echo(f"❌ 发送失败: {e}")
    
    # 记录历史
    try:
        get_history().add(text, voice, model_type, output_path, instruct)
    except:
        pass


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output-dir", "output_dir", help="输出目录", default="output")
@click.option("-v", "--voice", "voice", help="音色", default="female_young")
@click.option("-s", "--speed", "speed", help="语速", default=1.0, type=float)
@click.option("-m", "--model", "model_type", help="模型", default="qwen")
@click.option("--dry-run", is_flag=True, help="预览模式，不实际生成")
def batch(input_file, output_dir, voice, speed, model_type, dry_run):
    """批量合成 - 读取文本文件每行生成语音"""
    
    # 读取
    ext = Path(input_file).suffix.lower()
    if ext == ".json":
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                lines = [item.get("text", item.get("content", "")) for item in data]
            else:
                lines = [data.get("text", "")]
    else:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    
    lines = [l for l in lines if l]
    
    if not lines:
        click.echo("❌ 没有找到文本")
        return
    
    click.echo(f"📝 找到 {len(lines)} 条文本")
    
    if dry_run:
        for i, line in enumerate(lines, 1):
            click.echo(f"  [{i}] {line[:50]}...")
        return
    
    # 生成
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    engine = TTSEngine() if model_type == "qwen" else EdgeTTSEngine()
    
    success = 0
    errors = 0
    
    for i, line in enumerate(lines, 1):
        output_file = output_dir / f"output_{i:03d}.wav"
        try:
            click.echo(f"[{i}/{len(lines)}] ", nl=False)
            
            if model_type == "qwen":
                audio = engine.speak(text=line, voice=voice, speed=speed)
                engine.save(audio, str(output_file))
            else:
                engine.speak(line, voice, speed, output_file=str(output_file))
            
            success += 1
            click.echo(f"✅ {line[:30]}...")
            
        except Exception as e:
            errors += 1
            click.echo(f"❌ {line[:30]}... ({e})")
    
    click.echo(f"\n✅ 完成! 成功: {success}, 失败: {errors}")


@cli.command()
@click.argument("text")
@click.argument("ref_audio", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="输出文件", default="clone.wav")
@click.option("-s", "--speed", "speed", help="语速", default=1.0, type=float)
def clone(text, ref_audio, output_file, speed):
    """语音克隆 - 使用参考音频"""
    click.echo(f"🔊 语音克隆模式")
    click.echo(f"   文本: {text[:30]}...")
    click.echo(f"   参考: {ref_audio}")
    
    engine = TTSEngine()
    audio = engine.speak_clone(text, ref_audio, speed)
    engine.save(audio, output_file)
    click.echo(f"✅ 已保存到: {output_file}")


@cli.command()
@click.argument("text")
@click.option("-v", "--voice", "voice", help="音色", default="female_young")
@click.option("-s", "--speed", "speed", help="语速", default=1.0, type=float)
@click.option("-m", "--model", "model_type", help="模型", default="qwen")
def send(text, voice, speed, model_type):
    """生成语音并发送到飞书"""
    import tempfile
    
    tmp_file = f"/tmp/illli_send_{hash(text)}.wav"
    
    if model_type == "edge":
        engine = EdgeTTSEngine()
        mp3_file = tmp_file.replace(".wav", ".mp3")
        engine.speak(text, voice, speed, output_file=mp3_file)
        import subprocess
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", mp3_file, tmp_file], check=True, capture_output=True)
    elif model_type == "say":
        engine = TTSEngine()
        engine.speak_fallback(text, voice, tmp_file)
    else:
        engine = TTSEngine()
        audio = engine.speak(text=text, voice=voice, speed=speed)
        engine.save(audio, tmp_file)
    
    try:
        sender = FeishuSender()
        sender.send_audio(tmp_file, message=f"🎵 {text[:50]}...")
        click.echo("✅ 已发送到飞书!")
    except Exception as e:
        click.echo(f"❌ 发送失败: {e}")


@cli.command()
@click.option("-h", "--host", "host", default="0.0.0.0")
@click.option("-p", "--port", "port", default=8080, type=int)
def serve(host, port):
    """启动 HTTP API 服务"""
    from .api import app
    click.echo(f"🚀 API 服务: http://{host}:{port}")
    import uvicorn
    uvicorn.run(app, host=host, port=port)


@cli.command()
@click.option("-h", "--host", "host", default="0.0.0.0")
@click.option("-p", "--port", "port", default=7860, type=int)
def webui(host, port):
    """启动 Web 界面"""
    from .webui import launch_webui
    click.echo(f"🎨 Web 界面: http://{host}:{port}")
    launch_webui(server_name=host, server_port=port)


@cli.command()
@click.option("--limit", default=10, type=int)
def history(limit):
    """查看历史记录"""
    hist = get_history().list(limit)
    if not hist:
        click.echo("暂无历史记录")
        return
    
    for r in hist:
        time = r["timestamp"][:19].replace("T", " ")
        size = ""
        if os.path.exists(r.get("audio_path", "")):
            size = f" ({os.path.getsize(r['audio_path'])/1024:.0f}KB)"
        click.echo(f"[{r['id']}] {time} | {r['model']} | {r['voice']} | {r['text'][:35]}...{size}")


@cli.command()
def clear_history():
    """清空历史记录"""
    get_history().clear()
    click.echo("✅ 历史记录已清空")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="输出文件")
@click.option("--speed", "speed", default=1.0, type=float, help="语速")
@click.option("--pitch", "pitch", default=0, type=int, help="音调")
@click.option("--reverb", "reverb", is_flag=True, help="混响")
@click.option("--normalize/--no-normalize", default=True)
def process(input_file, output_file, speed, pitch, reverb, normalize):
    """音频后处理"""
    output_file = output_file or input_file
    
    click.echo(f"🔧 处理: {Path(input_file).name}")
    opts = []
    if speed != 1.0: opts.append(f"速度 {speed}x")
    if pitch != 0: opts.append(f"音调 {pitch}")
    if reverb: opts.append("混响")
    if opts:
        click.echo(f"   {' | '.join(opts)}")
    
    AudioProcessor.process_file(input_file, output_file, speed=speed, pitch=pitch, reverb=reverb, normalize=normalize)
    click.echo(f"✅ 已保存: {output_file}")


@cli.command()
def voices():
    """列出所有音色"""
    voices = {
        "female_young": "Vivian - 年轻女性",
        "female_cute": "Serena - 温柔女性",
        "male_young": "Dylan - 北京话男性",
        "male_mature": "Uncle_Fu - 成熟男性",
        "male_sichuan": "Eric - 四川话男性",
        "english_male": "Ryan - 英语男性",
        "english_male_2": "Aiden - 英语男性2",
        "japanese_female": "Ono_Anna - 日语女性",
        "korean_female": "Sohee - 韩语女性",
    }
    
    for vid, vinfo in voices.items():
        click.echo(f"  {vid}: {vinfo}")


@cli.command()
def status():
    """查看状态"""
    config = Config()
    manager = ModelManager()
    
    click.echo(f"版本: 0.2.0")
    click.echo(f"模型: {config.get('model.name')}")
    click.echo(f"模型目录: {config.get('model.cache_dir')}")
    click.echo(f"状态: {'✅ 已下载' if manager.is_model_downloaded() else '❌ 未下载'}")
    
    # 检查磁盘
    model_dir = Path(config.get('model.cache_dir'))
    if model_dir.exists():
        total = sum(f.stat().st_size for f in model_dir.rglob("*") if f.is_file()) / (1024**3)
        click.echo(f"占用: {total:.2f} GB")


@cli.command()
@click.argument("key", required=False)
@click.argument("value", required=False)
def config(key, value):
    """配置管理"""
    cfg = Config()
    
    if not key:
        import json
        click.echo(json.dumps(cfg.config, indent=2, ensure_ascii=False))
    elif not value:
        click.echo(cfg.get(key))
    else:
        cfg.set(key, value)
        cfg.save()
        click.echo(f"✅ 已设置 {key} = {value}")


@cli.command()
@click.argument("audio_file", type=click.Path(exists=True))
def play(audio_file):
    """播放音频"""
    import subprocess
    click.echo(f"🔊 播放: {audio_file}")
    subprocess.run(["afplay", audio_file])
    click.echo("✅ 播放完成")


@cli.command()
@click.argument("text")
@click.option("-v", "--voice", "voice", help="音色", default="female_young")
@click.option("-m", "--model", "model_type", help="模型", default="qwen")
def preview(text, voice, model_type):
    """快速预览 - 生成并播放"""
    import tempfile
    import subprocess
    
    tmp_file = tempfile.mktemp(suffix=".wav")
    
    click.echo(f"🔊 预览: {text[:30]}...")
    
    if model_type == "qwen":
        engine = TTSEngine()
        audio = engine.speak(text=text, voice=voice)
        engine.save(audio, tmp_file)
    else:
        engine = EdgeTTSEngine()
        mp3_file = tmp_file.replace(".wav", ".mp3")
        engine.speak(text, voice, 1.0, output_file=mp3_file)
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", mp3_file, tmp_file], capture_output=True)
    
    click.echo("🔊 播放中...")
    subprocess.run(["afplay", tmp_file])
    click.echo("✅ 完成")


@cli.command()
@click.option("-m", "--model", "model_type", help="模型", default="qwen")
def test(model_type):
    """测试所有音色"""
    test_text = "你好，这是一段测试语音。"
    
    voices = [
        ("female_young", "年轻女性 Vivian"),
        ("female_cute", "可爱女性 Serena"),
        ("male_young", "年轻男性 Dylan"),
        ("male_mature", "成熟男性 Uncle_Fu"),
        ("male_sichuan", "四川男性 Eric"),
        ("english_male", "英语男性 Ryan"),
        ("japanese_female", "日语女性 Ono_Anna"),
        ("korean_female", "韩语女性 Sohee"),
    ]
    
    click.echo(f"🧪 测试 {model_type} 模型的所有音色...\n")
    
    for vid, vname in voices:
        click.echo(f"  ▶ 测试 {vname}...", nl=False)
        
        tmp_file = f"/tmp/test_{vid}.wav"
        
        try:
            if model_type == "qwen":
                engine = TTSEngine()
                audio = engine.speak(text=test_text, voice=vid)
                engine.save(audio, tmp_file)
            else:
                engine = EdgeTTSEngine()
                mp3_file = tmp_file.replace(".wav", ".mp3")
                engine.speak(test_text, vid, 1.0, output_file=mp3_file)
                import subprocess
                subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", mp3_file, tmp_file], capture_output=True)
            
            click.echo(f"✅")
            # 自动播放
            import subprocess
            subprocess.run(["afplay", tmp_file], capture_output=True)
            
        except Exception as e:
            click.echo(f"❌ ({e})")
    
    click.echo("\n✅ 全部测试完成!")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_format")
def convert(input_file, output_format):
    """音频格式转换"""
    import subprocess
    
    input_path = Path(input_file)
    output_file = input_path.with_suffix(f".{output_format}")
    
    click.echo(f"🔄 转换: {input_path.name} -> {output_file.name}")
    
    # 使用 ffmpeg 转换
    subprocess.run([
        "ffmpeg", "-y", "-i", str(input_file),
        str(output_file)
    ], capture_output=True, check=True)
    
    click.echo(f"✅ 已保存: {output_file}")


@cli.command()
@click.argument("text")
@click.option("-l", "--lang", "target_lang", help="目标语言: zh/en/ja/ko", default="zh")
def translate(text, target_lang):
    """翻译并生成语音 (需要网络)"""
    try:
        from googletrans import Translator
    except ImportError:
        click.echo("❌ 请安装: pip install googletrans")
        return
    
    translator = Translator()
    result = translator.translate(text, dest=target_lang)
    
    click.echo(f"原文: {text}")
    click.echo(f"翻译: {result.text}")
    click.echo(f"语言: {result.src} -> {target_lang}")
    
    # 生成语音
    click.echo("\n🎵 生成语音...")
    engine = TTSEngine()
    audio = engine.speak(text=result.text, voice="female_young")
    output_file = f"/tmp/translate_{hash(text)}.wav"
    engine.save(audio, output_file)
    click.echo(f"✅ 已保存: {output_file}")


@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", "output_file", help="输出文件")
@click.option("--sample-rate", "sample_rate", default=24000, type=int, help="采样率")
def resample(input_file, output_file, sample_rate):
    """调整采样率"""
    import subprocess
    
    if not output_file:
        input_path = Path(input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_sr{sample_rate}{input_path.suffix}")
    
    click.echo(f"🔄 调整采样率: {sample_rate}Hz")
    
    subprocess.run([
        "ffmpeg", "-y", "-i", input_file,
        "-ar", str(sample_rate),
        output_file
    ], capture_output=True, check=True)
    
    click.echo(f"✅ 已保存: {output_file}")


@cli.command()
@click.argument("text")
def ssml(text):
    """SSML 文本转语音 (高级)"""
    # 简化版 SSML 支持
    import re
    
    # 移除标签，获取纯文本用于预览
    plain_text = re.sub(r'<[^>]+>', '', text)
    click.echo(f"📝 SSML 内容:\n{plain_text[:100]}...")
    
    # TODO: 实现完整 SSML 支持
    click.echo("⚠️ SSML 功能开发中...")


@cli.command()
def info():
    """显示项目信息"""
    click.echo("""
🎤 illli-tts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
版本: 0.2.0
模型: Qwen3-TTS-1.7B-CustomVoice
平台: Apple Silicon (MPS)

📦 功能:
  speak      语音合成
  batch      批量合成
  clone      语音克隆
  preview    快速预览
  test       音色测试
  play       播放音频
  convert    格式转换
  process    后处理
  serve      API 服务
  webui      Web 界面

🔗 链接:
  GitHub: https://github.com/illli-studio/illli-tts
""")




def main():
    cli()


@cli.command()
@click.argument("text")
def count(text):
    """统计文本"""
    import re
    c = len(re.findall(r'[\u4e00-\u9fff]', text))
    e = len(re.findall(r'[a-zA-Z]', text))
    click.echo(f"字符: {len(text)} | 中文: {c} | 英文: {e}")


@cli.command()
@click.argument("text")
def clean(text):
    """清理文本"""
    import re
    click.echo(re.sub(r'\s+', ' ', text).strip())


if __name__ == "__main__":
    main()
