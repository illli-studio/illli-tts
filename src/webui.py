"""Web 界面模块 - Gradio"""

import gradio as gr
from pathlib import Path
import tempfile

from .tts import TTSEngine
from .edge_tts_engine import EdgeTTSEngine


# 可用音色
VOICES = [
    ("年轻女性 (Vivian)", "female_young"),
    ("可爱女性 (Serena)", "female_cute"),
    ("年轻男性 (Dylan)", "male_young"),
    ("成熟男性 (Uncle_Fu)", "male_mature"),
    ("四川男性 (Eric)", "male_sichuan"),
    ("英语男性 (Ryan)", "english_male"),
    ("英语男性2 (Aiden)", "english_male_2"),
    ("日语女性 (Ono_Anna)", "japanese_female"),
    ("韩语女性 (Sohee)", "korean_female"),
]

# 模型选项
MODELS = ["qwen", "edge", "say"]


def tts_generator(text, voice, speed, model, instruct):
    """生成语音"""
    if not text.strip():
        return None, "请输入文字"
    
    output_path = f"/tmp/gradio_{hash(text)}.wav"
    
    try:
        if model == "qwen":
            engine = TTSEngine()
            audio = engine.speak(
                text=text,
                voice=voice,
                speed=speed,
                instruct=instruct if instruct else None,
            )
            engine.save(audio, output_path)
        elif model == "edge":
            engine = EdgeTTSEngine()
            engine.speak(text, voice, speed, output_file=output_path)
        else:
            engine = TTSEngine()
            engine.speak_fallback(text, voice, output_path)
        
        return output_path, "✅ 生成成功!"
        
    except Exception as e:
        return None, f"❌ 生成失败: {str(e)}"


def create_webui():
    """创建 Web 界面"""
    with gr.Blocks(title="illli-tts", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🎤 illli-tts 文字转语音")
        gr.Markdown("基于 Qwen3-TTS 的语音合成工具")
        
        with gr.Row():
            with gr.Column():
                text_input = gr.Textbox(
                    label="输入文字",
                    placeholder="请输入要转换的文字...",
                    lines=4
                )
                
                voice_input = gr.Dropdown(
                    choices=VOICES,
                    value="female_young",
                    label="选择音色"
                )
                
                model_input = gr.Radio(
                    choices=MODELS,
                    value="qwen",
                    label="选择模型"
                )
                
                speed_input = gr.Slider(
                    minimum=0.5,
                    maximum=2.0,
                    value=1.0,
                    step=0.1,
                    label="语速"
                )
                
                instruct_input = gr.Textbox(
                    label="语音指令 (可选)",
                    placeholder="如: 用温柔的语气, 撒娇的语气...",
                    lines=2
                )
                
                generate_btn = gr.Button("🎵 生成语音", variant="primary")
            
            with gr.Column():
                audio_output = gr.Audio(label="生成的语音")
                status_output = gr.Textbox(label="状态", lines=2)
        
        generate_btn.click(
            fn=tts_generator,
            inputs=[text_input, voice_input, speed_input, model_input, instruct_input],
            outputs=[audio_output, status_output]
        )
        
        # 示例
        gr.Examples(
            examples=[
                ["你好，我是小灵", "female_young", "qwen", "1.0", ""],
                ["哥哥，你回来啦！", "female_young", "qwen", "1.0", "用撒娇的语气"],
                ["Hello, world!", "english_male", "qwen", "1.0", ""],
            ],
            inputs=[text_input, voice_input, model_input, speed_input, instruct_input],
        )
    
    return demo


def launch_webui(server_name="0.0.0.0", server_port=7860):
    """启动 Web 界面"""
    demo = create_webui()
    demo.launch(server_name=server_name, server_port=server_port)


if __name__ == "__main__":
    launch_webui()
