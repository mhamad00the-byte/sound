import gradio as gr
import edge_tts
import asyncio
import tempfile
import os
import uuid

import streamlit as st
import gradio as gr

# ئەم بەشەی خوارەوە بۆ پیشاندانی Gradio لەسەر Streamlitـە
with gr.Blocks() as demo:
    pass # یان ناوی ڕووکارەکەی خۆت بنووسە

# داگیرساندنی ڕاستەوخۆ لە Streamlit
import streamlit.components.v1 as components
demo.launch(prevent_thread_lock=True)
components.iframe(f"http://localhost:7860", height=800)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def get_voices():
    voices = await edge_tts.list_voices()
    return {f"{v['ShortName']} - {v['Locale']} ({v['Gender']})": v['ShortName'] for v in voices}

async def text_to_speech(text, voice, rate, pitch):
    if not text.strip():
        return None, None, "Please enter text to convert."
    if not voice:
        return None, None, "Please select a voice."
    
    voice_short_name = voice.split(" - ")[0]
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"
    communicate = edge_tts.Communicate(text, voice_short_name, rate=rate_str, pitch=pitch_str)
    
    file_id = uuid.uuid4().hex[:10]
    output_path = os.path.join(OUTPUT_DIR, f"speech_{file_id}.mp3")
    await communicate.save(output_path)
    
    return output_path, output_path, None

async def tts_interface(text, voice, rate, pitch):
    audio, file_download, warning = await text_to_speech(text, voice, rate, pitch)
    if warning:
        return audio, file_download, gr.Warning(warning)
    return audio, file_download, None

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

body, .gradio-container {
    background: #090d16 !important;
    color: #f1f5f9 !important;
}

/* Container width & alignment */
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    padding: 30px 20px !important;
}

/* Hide Gradio default footer */
footer {
    display: none !important;
}

/* Studio Glass Card */
.studio-card {
    background: rgba(17, 24, 39, 0.8) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
}

/* Header Section */
.header-box {
    text-align: center;
    margin-bottom: 28px;
}

.hero-title {
    background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    margin-bottom: 8px !important;
}

.hero-subtitle {
    color: #94a3b8 !important;
    font-size: 1rem !important;
    margin: 0 auto 16px auto !important;
}

/* Badges */
.badge-group {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 12px;
}

.badge {
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

.badge-purple {
    background: rgba(139, 92, 246, 0.15);
    color: #c084fc;
    border: 1px solid rgba(139, 92, 246, 0.3);
}

.badge-blue {
    background: rgba(59, 130, 246, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

/* Form Inputs */
.gradio-container textarea, 
.gradio-container input, 
.gradio-container select {
    background-color: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
}

.gradio-container textarea:focus, 
.gradio-container input:focus, 
.gradio-container select:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}

/* Sliders */
.gradio-container input[type="range"] {
    accent-color: #818cf8 !important;
}

/* Primary Button */
#generate-btn {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #d946ef 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    border-radius: 16px !important;
    padding: 16px 32px !important;
    cursor: pointer !important;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
    margin-top: 8px !important;
}

#generate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 35px rgba(124, 58, 237, 0.55) !important;
    filter: brightness(1.1) !important;
}

#generate-btn:active {
    transform: translateY(0) !important;
}

/* Output Audio Container */
.output-box {
    background: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 18px !important;
    padding: 20px !important;
    margin-top: 20px !important;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* File Download Styling */
.gradio-container .file-preview {
    background-color: #1e293b !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
"""

async def create_demo():
    voices = await get_voices()
    default_voice = next((k for k in voices.keys() if "en-US-AndrewMultilingualNeural" in k), "en-US-AndrewMultilingualNeural - en-US (Male)")
    
    with gr.Blocks(analytics_enabled=False, title="Edge TTS Studio") as demo:
        
        with gr.Column(elem_classes=["studio-card"]):
            # Header
            gr.HTML("""
            <div class="header-box">
                <div class="badge-group">
                    <span class="badge badge-purple">⚡ Edge TTS Neural</span>
                    <span class="badge badge-blue">🎙️ High Quality</span>
                </div>
                <h1 class="hero-title">Text-to-Speech Studio</h1>
                <p class="hero-subtitle">Convert script to audio using Microsoft Edge AI voices with custom rate & pitch adjustment.</p>
            </div>
            """)
            
            # Input Text Area
            text_input = gr.Textbox(
                label="Input Text", 
                placeholder="Enter or paste text here...", 
                lines=5
            )
            
            # Voice Dropdown
            voice_dropdown = gr.Dropdown(
                choices=[""] + list(voices.keys()), 
                label="Select Voice", 
                value=default_voice
            )
            
            # Rate & Pitch Controls
            with gr.Row():
                rate_slider = gr.Slider(
                    minimum=-50, 
                    maximum=50, 
                    value=-3, 
                    label="Speech Rate Adjustment (%)", 
                    step=1
                )
                pitch_slider = gr.Slider(
                    minimum=-20, 
                    maximum=20, 
                    value=-5, 
                    label="Pitch Adjustment (Hz)", 
                    step=1
                )
            
            # Generate Button
            generate_btn = gr.Button("✨ Generate Speech", elem_id="generate-btn", variant="primary")
            warning_md = gr.Markdown(visible=False)
            
            # Audio Output Player & Download File Button
            with gr.Group(elem_classes=["output-box"]):
                gr.HTML('<div class="section-title">🎧 Generated Audio Output</div>')
                audio_output = gr.Audio(label="Audio Preview", type="filepath", interactive=False)
                file_download = gr.File(label="⬇️ Download MP3 File Directly", interactive=False)

        # Click event
        generate_btn.click(
            fn=tts_interface,
            inputs=[text_input, voice_dropdown, rate_slider, pitch_slider],
            outputs=[audio_output, file_download, warning_md]
        )
        
    return demo

async def main():
    demo = await create_demo()
    demo.queue(default_concurrency_limit=50)
    demo.launch(css=CUSTOM_CSS, allowed_paths=[OUTPUT_DIR])

if __name__ == "__main__":
    asyncio.run(main())
