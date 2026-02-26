"""CLI 入口 - illli-tts 命令行工具"""

import sys
import click
from pathlib import Path

from .tts import TTSEngine
from .edge_tts import EdgeTTSEngine
from .models import ModelManager
from .voices import VoiceManager
from .sender import FeishuSender
from .config import Config


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """illli-tts: 基于 Qwen3-TTS 的文字转语音工具"""
    pass


@cli.command()
@click.argument("text")
@click.option("-o", "--output", "output_file", help="输出音频文件路径", default="output.wav")
@click.option("-v", "--voice", "voice", help="音色名称", default="female_young")
@click.option("-s", "--speed", "speed", help="语速 (0.5-2.0)", default=1.0)
@click.option("-m", "--model", "model_type", help="模型类型: edge/qwen/say", default="edge")
@click.option("--ref-audio", "ref_audio", help="参考音频路径 (用于语音克隆)", default=None)
@click.option("--voice-desc", "voice_desc", help="语音描述 (用于语音设计)", default=None)
def speak(text, output_file, voice, speed, model_type, ref_audio, voice_desc):
    """将文字转为语音"""
    
    if model_type == "edge":
        # 使用 Edge TTS (默认，推荐)
        click.echo(f"🎵 使用 Edge TTS ({voice})...")
        engine = EdgeTTSEngine()
        output_path = engine.speak(text, voice, speed, output_file=output_file)
        
        # 转换为 WAV
        if output_path.endswith(".mp3"):
            import subprocess
            wav_path = output_path.replace(".mp3", ".wav")
            subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", output_path, wav_path], check=True)
            output_file = wav_path
        
        click.echo(f"✅ 已保存到: {output_file}")
        
    elif model_type == "say":
        # 使用 macOS say 命令
        click.echo(f"🎤 使用 macOS say ({voice})...")
        engine = TTSEngine()
        output_file = engine.speak_fallback(text, voice, output_file)
        click.echo(f"✅ 已保存到: {output_file}")
        
    elif model_type == "qwen":
        # 使用 Qwen3-TTS 模型 (需要下载模型)
        click.echo(f"🧠 使用 Qwen3-TTS 模型 ({voice})...")
        engine = TTSEngine()
        audio = engine.speak(
            text=text,
            voice=voice,
            speed=speed,
            ref_audio=ref_audio,
            voice_desc=voice_desc
        )
        engine.save(audio, output_file)
        click.echo(f"✅ 已保存到: {output_file}")
    
    else:
        click.echo(f"❌ 未知模型类型: {model_type}")
        click.echo("可用类型: edge, say, qwen")


@cli.command()
@click.argument("text")
@click.option("-v", "--voice", "voice", help="音色名称", default="female_young")
@click.option("-s", "--speed", "speed", help="语速 (0.5-2.0)", default=1.0)
@click.option("-m", "--model", "model_type", help="模型类型: edge/say/qwen", default="edge")
def send(text, voice, speed, model_type):
    """生成语音并发送到飞书 (需要配置飞书应用)"""
    click.echo(f"🎵 正在生成语音...")
    
    if model_type == "edge":
        engine = EdgeTTSEngine()
        temp_file = engine.speak(text, voice, speed, output_file="/tmp/illli-edge-send.mp3")
        # 转换 MP3 到 WAV
        import subprocess
        wav_file = "/tmp/illli-edge-send.wav"
        subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16", temp_file, wav_file], check=True)
        temp_file = wav_file
    elif model_type == "say":
        engine = TTSEngine()
        temp_file = engine.speak_fallback(text, voice, "/tmp/illli-say-send.wav")
    else:
        engine = TTSEngine()
        audio = engine.speak(text=text, voice=voice, speed=speed)
        temp_file = "/tmp/illli-tts-output.wav"
        engine.save(audio, temp_file)
    
    click.echo(f"✅ 语音已生成: {temp_file}")
    click.echo("📤 提示: 请配置飞书应用密钥才能自动发送")
    click.echo(f"   或者直接用命令: illli-tts speak \"{text}\" -o {temp_file}")
    click.echo("   然后手动发送到飞书")


@cli.command()
def download():
    """下载模型"""
    click.echo("📥 正在下载模型...")
    
    manager = ModelManager()
    manager.download()
    
    click.echo("✅ 模型下载完成！")


@cli.command()
def voices():
    """列出所有可用的音色"""
    manager = VoiceManager()
    voices = manager.list_voices()
    
    click.echo("🎭 可用音色:")
    for voice_id, info in voices.items():
        click.echo(f"  • {voice_id}: {info['name']} - {info['description']}")


@cli.command()
def status():
    """查看模型状态"""
    config = Config()
    
    click.echo("📊 illli-tts 状态:")
    click.echo(f"  模型: {config.get('model.name')}")
    click.echo(f"  下载源: {config.get('model.download_source')}")
    click.echo(f"  模型目录: {config.get('model.cache_dir')}")
    
    # 检查模型是否存在
    manager = ModelManager()
    if manager.is_model_downloaded():
        click.echo("  状态: ✅ 已下载")
    else:
        click.echo("  状态: ❌ 未下载 (运行 'illli-tts download' 下载)")


def main():
    cli()


if __name__ == "__main__":
    main()
