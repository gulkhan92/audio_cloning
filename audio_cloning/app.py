"""
Professional Audio Cloning Streamlit Application.
A high-quality voice cloning web app using Coqui TTS.
"""
import streamlit as st
import logging
import os
from pathlib import Path
from datetime import datetime
import numpy as np
import soundfile as sf

# Import utilities
from models.schemas import VoiceCloneRequest, TTSResponse
from utils.voice_clone import VoiceClone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Voice Cloning Pro",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
CUSTOM_CSS = """
<style>
    /* Main theme - Dark gradient background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }
    
    /* Title styling */
    .title-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .title-container h1 {
        font-size: 3.5rem;
        background: linear-gradient(90deg, #00d9ff, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .title-container p {
        color: #b0b0b0;
        font-size: 1.2rem;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        box-shadow: 0 12px 40px rgba(0, 217, 255, 0.2);
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(168, 85, 247, 0.5);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d9ff 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 217, 255, 0.5);
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #ffffff;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        color: #ffffff;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00d9ff;
        box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00d9ff 0%, #a855f7 100%);
        border-color: #00d9ff;
        color: white !important;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px;
        padding: 1rem;
    }
    
    .stSuccess {
        background: rgba(0, 255, 136, 0.15);
        border: 1px solid rgba(0, 255, 136, 0.5);
        color: #00ff88;
    }
    
    .stError {
        background: rgba(255, 0, 85, 0.15);
        border: 1px solid rgba(255, 0, 85, 0.5);
        color: #ff0055;
    }
    
    .stWarning {
        background: rgba(255, 153, 0, 0.15);
        border: 1px solid rgba(255, 153, 0, 0.5);
        color: #ff9900;
    }
    
    .stInfo {
        background: rgba(0, 217, 255, 0.15);
        border: 1px solid rgba(0, 217, 255, 0.5);
        color: #00d9ff;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px dashed rgba(255, 255, 255, 0.2);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d9ff, #a855f7);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00d9ff !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0, 217, 255, 0.4); }
        50% { box-shadow: 0 0 0 10px rgba(0, 217, 255, 0); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Info box */
    .info-box {
        background: rgba(0, 217, 255, 0.1);
        border-left: 4px solid #00d9ff;
        padding: 1.5rem;
        border-radius: 0 15px 15px 0;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    /* General text */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, label {
        color: #ffffff !important;
    }
    
    /* Checkbox and radio */
    .stCheckbox label,
    .stRadio div {
        color: #ffffff !important;
    }
    
    /* Slider */
    .stSlider label {
        color: #ffffff !important;
    }
    
    /* Caption */
    .stCaption {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 10px;
    }
    
    /* Waveform visualization placeholder */
    .waveform-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
"""

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


class SessionState:
    """Session state manager for the application."""
    
    @staticmethod
    def init():
        """Initialize session state variables."""
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'current_audio' not in st.session_state:
            st.session_state.current_audio = None


def create_directories():
    """Create necessary directories."""
    dirs = ['outputs', 'temp']
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)


def render_header():
    """Render the application header."""
    st.markdown("""
    <div class="title-container fade-in">
        <h1>🎤 Voice Cloning Pro</h1>
        <p>Clone any voice and generate speech with AI</p>
    </div>
    """, unsafe_allow_html=True)


def render_features():
    """Render feature highlights."""
    st.markdown("### ✨ Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card fade-in" style="animation-delay: 0.1s;">
            <div class="feature-icon">🔊</div>
            <h4>High Quality</h4>
            <p style="color: #b0b0b0; font-size: 0.9rem;">Studio-quality audio output</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card fade-in" style="animation-delay: 0.2s;">
            <div class="feature-icon">🌍</div>
            <h4>Multi-Language</h4>
            <p style="color: #b0b0b0; font-size: 0.9rem;">Support for 10+ languages</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card fade-in" style="animation-delay: 0.3s;">
            <div class="feature-icon">⚡</div>
            <h4>Fast Processing</h4>
            <p style="color: #b0b0b0; font-size: 0.9rem;">Quick voice cloning</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card fade-in" style="animation-delay: 0.4s;">
            <div class="feature-icon">🔒</div>
            <h4>Secure</h4>
            <p style="color: #b0b0b0; font-size: 0.9rem;">Your data stays private</p>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with app info."""
    with st.sidebar:
        st.markdown("### 🎤 App Info")
        st.info("""
        **Voice Cloning Pro**
        
        Clone any voice from a short audio sample and generate natural speech.
        """)
        
        st.markdown("### ⚙️ Settings")
        
        # Model info
        st.markdown("**Model:** YourTTS")
        st.caption("Coqui TTS multilingual model")
        
        st.markdown("### 📊 Statistics")
        
        if st.session_state.get('history'):
            total_clones = len(st.session_state.history)
            st.metric("Total Clones", total_clones)
        else:
            st.metric("Total Clones", 0)
        
        st.markdown("---")
        st.markdown("### 📖 Guide")
        with st.expander("How to use"):
            st.markdown("""
            **Getting Started:**
            
            1. **Upload Voice Sample** - Upload a clear audio recording (5-30 seconds)
            
            2. **Enter Text** - Type the text you want the cloned voice to speak
            
            3. **Clone Voice** - Click the button to generate
            
            **Tips for Best Results:**
            - Use clean, clear audio without background noise
            - 10-30 seconds works best
            - Single speaker audio produces better results
            - The voice should be in the language you want to speak
            """)
        
        with st.expander("Supported Languages"):
            languages = VoiceClone.get_supported_languages()
            for code, name in languages.items():
                st.markdown(f"- **{code.upper()}**: {name}")


def render_voice_clone():
    """Render Voice Cloning main interface."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <strong>🎯 How it works:</strong> Upload a voice reference (5-30 seconds), enter your text, 
        and our AI will generate speech that sounds like the reference voice.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎤 Reference Voice")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload voice sample (MP3, WAV, OGG)",
            type=['mp3', 'wav', 'ogg'],
            key="clone_audio"
        )
        
        if uploaded_file:
            # Save uploaded file temporarily
            temp_dir = Path("temp")
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            temp_audio_path = temp_dir / f"ref_{uploaded_file.name}"
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Validate audio
            voice_clone = VoiceClone()
            validation = voice_clone.validate_reference_audio(str(temp_audio_path))
            
            if validation.get("valid"):
                st.success(f"✅ Audio valid: {validation['duration']}s, {validation['sample_rate']}Hz")
                
                # Show audio info
                st.markdown("#### 📊 Audio Details")
                info_col1, info_col2, info_col3 = st.columns(3)
                with info_col1:
                    st.metric("Duration", f"{validation['duration']}s")
                with info_col2:
                    st.metric("Sample Rate", f"{validation['sample_rate']}Hz")
                with info_col3:
                    st.metric("Channels", validation['channels'].title())
                
                # Preview audio
                st.markdown("#### 👂 Preview")
                st.audio(str(temp_audio_path), format="audio/wav")
            else:
                st.error(f"❌ Invalid audio: {validation.get('message')}")
                
    with col2:
        st.markdown("### 🌍 Language & Settings")
        
        # Language selection
        languages = VoiceClone.get_supported_languages()
        language = st.selectbox(
            "Output Language",
            options=list(languages.keys()),
            format_func=lambda x: f"{languages[x]} ({x.upper()})",
            key="clone_language"
        )
        
        st.markdown("#### 📝 Text Input")
        
        # Text input
        text_input = st.text_area(
            "Text to speak",
            height=200,
            placeholder="Enter the text you want the cloned voice to speak...",
            key="clone_text",
            max_chars=2000
        )
        
        if text_input:
            char_count = len(text_input)
            st.caption(f"Characters: {char_count}/2000")
            
            # Character limit warning
            if char_count > 1500:
                st.warning("⚠️ Long text may take longer to process.")
    
    st.markdown("---")
    
    # Clone button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        clone_button = st.button(
            "🎵 Clone Voice", 
            key="clone_voice",
            disabled=not (uploaded_file and text_input and text_input.strip())
        )
    
    if clone_button:
        if not uploaded_file:
            st.error("Please upload a reference audio file.")
        elif not text_input.strip():
            st.error("Please enter some text to speak.")
        else:
            with st.spinner("🎤 Cloning voice... This may take a moment."):
                try:
                    # Create request
                    request = VoiceCloneRequest(
                        text=text_input,
                        language=language
                    )
                    
                    # Clone voice
                    voice_clone = VoiceClone()
                    result = voice_clone.clone_voice(
                        request=request,
                        reference_audio_path=str(temp_audio_path)
                    )
                    
                    if result.success:
                        st.success("✅ " + result.message)
                        
                        # Display audio player
                        st.markdown("### 🔊 Generated Audio")
                        st.audio(result.file_path, format="audio/wav")
                        
                        # Download button
                        col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
                        with col_d2:
                            with open(result.file_path, "rb") as f:
                                st.download_button(
                                    label="⬇️ Download Audio",
                                    data=f.read(),
                                    file_name="cloned_voice.wav",
                                    mime="audio/wav"
                                )
                        
                        # Add to history
                        st.session_state.history.append({
                            "type": "Voice Cloning",
                            "text": text_input[:100] + "...",
                            "language": language,
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        # Show success animation
                        st.balloons()
                        
                    else:
                        st.error(f"❌ Error: {result.error}")
                        
                except Exception as e:
                    st.error(f"❌ Voice cloning failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_history():
    """Render conversion history."""
    st.markdown("### 📜 Recent Clones")
    
    if st.session_state.get('history'):
        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"🎤 {item['type']} - {item['timestamp'][:19]}"):
                st.markdown(f"**Text:** {item['text']}")
                st.markdown(f"**Language:** {item['language'].upper()}")
                st.markdown(f"**Time:** {item['timestamp'][:19]}")
    else:
        st.info("No voice clones yet. Start using the app to clone your voice!")


def render_faq():
    """Render FAQ section."""
    st.markdown("### ❓ Frequently Asked Questions")
    
    with st.expander("What is voice cloning?"):
        st.markdown("""
        Voice cloning is a technology that uses AI to replicate a person's voice. 
        By analyzing a short audio sample, our system can generate new speech that sounds 
        like the original speaker.
        """)
    
    with st.expander("How long should the reference audio be?"):
        st.markdown("""
        For best results, use 10-30 seconds of clear audio. Shorter samples (3-5 seconds) 
        can work but may produce less accurate results. Longer samples don't necessarily 
        improve quality.
        """)
    
    with st.expander("What audio formats are supported?"):
        st.markdown("""
        We support MP3, WAV, and OGG formats. For best results, use WAV files with 
        a sample rate of 22050Hz or higher.
        """)
    
    with st.expander("Is my data secure?"):
        st.markdown("""
        Yes! All audio processing is done locally. Your voice samples and generated 
        audio are not stored on any server. Everything stays on your device.
        """)


def main():
    """Main application function."""
    # Initialize
    SessionState.init()
    create_directories()
    
    # Render header
    render_header()
    
    # Render features
    render_features()
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    tabs = st.tabs([
        "🎤 Voice Cloning",
        "📜 History",
        "❓ FAQ"
    ])
    
    with tabs[0]:
        render_voice_clone()
    
    with tabs[1]:
        render_history()
    
    with tabs[2]:
        render_faq()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: rgba(255,255,255,0.5); padding: 1rem;'>"
        "🎤 Voice Cloning Pro | Powered by Coqui TTS | © 2026"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

