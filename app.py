"""
Main Streamlit application for Text to Speech Pro.
A professional TTS application with multiple modes: Basic, Advanced, and Voice Cloning.
"""
import streamlit as st
import logging
import os
from pathlib import Path
from datetime import datetime

# Import utilities and models
from models.schemas import BasicTTSRequest, AdvancedTTSRequest, VoiceCloneRequest
from utils.tts_basic import BasicTTS
from utils.tts_advanced import AdvancedTTS
from utils.voice_clone import VoiceClone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Text to Speech Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
CUSTOM_CSS = """
<style>
    /* Main theme - Light background for better readability */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1a1a2e !important;
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
        font-size: 3rem;
        background: linear-gradient(90deg, #e94560, #0f3460);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .title-container p {
        color: #333333;
        font-size: 1.2rem;
    }
    
    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .card:hover {
        border-color: rgba(233, 69, 96, 0.5);
        box-shadow: 0 8px 32px rgba(233, 69, 96, 0.2);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #c73e54 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(233, 69, 96, 0.4);
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(0, 0, 0, 0.2);
        color: #1a1a2e;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: rgba(240, 240, 240, 0.9);
    }
    
    /* Input styling - Light background with dark text */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        color: #1a1a2e;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #666666;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #e94560;
        box-shadow: 0 0 0 2px rgba(233, 69, 96, 0.2);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {
        color: #1a1a2e !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: 1px solid rgba(0, 0, 0, 0.1);
        color: #1a1a2e;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #e94560 0%, #c73e54 100%);
        border-color: #e94560;
        color: white !important;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stSuccess {
        background: rgba(0, 255, 128, 0.15);
        border: 1px solid rgba(0, 255, 128, 0.5);
        color: #006644;
    }
    
    .stError {
        background: rgba(255, 0, 85, 0.15);
        border: 1px solid rgba(255, 0, 85, 0.5);
        color: #cc0000;
    }
    
    .stWarning {
        background: rgba(255, 153, 0, 0.15);
        border: 1px solid rgba(255, 153, 0, 0.5);
        color: #994d00;
    }
    
    .stInfo {
        background: rgba(51, 153, 255, 0.15);
        border: 1px solid rgba(51, 153, 255, 0.5);
        color: #004080;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 1rem;
        border: 1px dashed rgba(0, 0, 0, 0.2);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #e94560, #f5af19);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #e94560;
    }
    
    [data-testid="stMetricLabel"] {
        color: #333333;
    }
    
    /* Divider */
    hr {
        border-color: rgba(0, 0, 0, 0.1);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Custom container */
    .feature-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(233, 69, 96, 0.5);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Audio player */
    audio {
        width: 100%;
        border-radius: 10px;
    }
    
    /* Info box */
    .info-box {
        background: rgba(233, 69, 96, 0.1);
        border-left: 4px solid #e94560;
        padding: 1rem;
        border-radius: 0 10px 10px 0;
        margin: 1rem 0;
        color: #1a1a2e;
    }
    
    /* General text color for Streamlit elements */
    .stMarkdown {
        color: #1a1a2e !important;
    }
    
    p, label {
        color: #1a1a2e !important;
    }
    
    /* Checkbox and radio button text */
    .stCheckbox label,
    .stRadio div {
        color: #1a1a2e !important;
    }
    
    /* Slider text */
    .stSlider label {
        color: #1a1a2e !important;
    }
    
    /* Caption text */
    .stCaption {
        color: #666666 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #1a1a2e !important;
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
        if 'current_tab' not in st.session_state:
            st.session_state.current_tab = "Basic TTS"


def create_directories():
    """Create necessary directories."""
    dirs = ['outputs', 'temp']
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)


def render_header():
    """Render the application header."""
    st.markdown("""
    <div class="title-container fade-in">
        <h1>🎙️ Text to Speech Pro</h1>
        <p>Professional Text-to-Speech Converter with Voice Cloning</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with app info."""
    with st.sidebar:
        st.markdown("### 📱 App Info")
        st.info("""
        **Text to Speech Pro**
        
        Convert your text to speech with multiple engines and voice cloning capabilities.
        """)
        
        st.markdown("### ⚙️ Settings")
        
        # Theme toggle
        dark_mode = st.toggle("Dark Mode", value=True)
        
        st.markdown("### 📊 Statistics")
        
        if st.session_state.get('history'):
            total_conversions = len(st.session_state.history)
            st.metric("Total Conversions", total_conversions)
        else:
            st.metric("Total Conversions", 0)
        
        st.markdown("---")
        st.markdown("### ℹ️ Help")
        with st.expander("How to use"):
            st.markdown("""
            1. **Basic TTS**: Quick text-to-speech using Google
            2. **Advanced TTS**: High-quality Coqui TTS
            3. **Voice Cloning**: Clone voice from reference audio
            
            **Tips:**
            - Use 5-10 second audio for voice cloning
            - Clear audio produces better results
            """)


def render_basic_tts():
    """Render Basic TTS tab."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Enter Text")
        text_input = st.text_area(
            "Text to convert",
            height=200,
            placeholder="Enter the text you want to convert to speech...",
            key="basic_text"
        )
    
    with col2:
        st.markdown("### ⚡ Settings")
        
        # Language selection
        basic_tts = BasicTTS()
        languages = basic_tts.get_supported_languages()
        language = st.selectbox(
            "Language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            key="basic_language"
        )
        
        # Speed option
        slow = st.checkbox("Slow speech", value=False, key="basic_slow")
        
        # Character count
        if text_input:
            char_count = len(text_input)
            st.caption(f"Characters: {char_count}")
            
            if char_count > 5000:
                st.warning("⚠️ Text exceeds 5000 characters. It will be truncated.")
    
    st.markdown("---")
    
    # Convert button
    if st.button("🎵 Convert to Speech", key="basic_convert"):
        if not text_input.strip():
            st.error("Please enter some text to convert.")
        else:
            with st.spinner("Converting text to speech..."):
                try:
                    # Validate and create request
                    request = BasicTTSRequest(
                        text=text_input[:5000],  # Truncate if too long
                        language=language,
                        slow=slow
                    )
                    
                    # Convert
                    tts = BasicTTS()
                    result = tts.convert(request)
                    
                    if result.success:
                        st.success(result.message)
                        
                        # Display audio player
                        st.markdown("### 🎧 Generated Audio")
                        st.audio(result.file_path, format="audio/mp3")
                        
                        # Download button
                        with open(result.file_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Audio",
                                data=f.read(),
                                file_name="tts_output.mp3",
                                mime="audio/mp3"
                            )
                        
                        # Add to history
                        st.session_state.history.append({
                            "type": "Basic TTS",
                            "text": text_input[:100] + "...",
                            "language": language,
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        st.error(f"Error: {result.error}")
                        
                except Exception as e:
                    st.error(f"Conversion failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_advanced_tts():
    """Render Advanced TTS tab."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📝 Enter Text")
        text_input = st.text_area(
            "Text to convert",
            height=200,
            placeholder="Enter high-quality text-to-speech...",
            key="advanced_text"
        )
    
    with col2:
        st.markdown("### ⚡ Settings")
        
        # Model selection
        advanced_tts = AdvancedTTS()
        models = advanced_tts.get_available_models()
        
        model_name = st.selectbox(
            "TTS Model",
            options=list(models.keys()),
            format_func=lambda x: f"{models[x]['name']} ({x})",
            key="advanced_model"
        )
        
        # Show model description
        st.caption(models[model_name]['description'])
        
        # Speed
        speed = st.slider("Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        
        # Character count
        if text_input:
            char_count = len(text_input)
            st.caption(f"Characters: {char_count}")
    
    st.markdown("---")
    
    # Convert button
    if st.button("🎵 Generate Speech", key="advanced_convert"):
        if not text_input.strip():
            st.error("Please enter some text to convert.")
        else:
            with st.spinner("Generating high-quality speech... This may take a moment."):
                try:
                    # Validate and create request
                    request = AdvancedTTSRequest(
                        text=text_input,
                        model_name=model_name,
                        speed=speed
                    )
                    
                    # Convert
                    tts = AdvancedTTS()
                    result = tts.convert(request)
                    
                    if result.success:
                        st.success(result.message)
                        
                        # Display audio player
                        st.markdown("### 🎧 Generated Audio")
                        st.audio(result.file_path, format="audio/wav")
                        
                        # Download button
                        with open(result.file_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Audio",
                                data=f.read(),
                                file_name="advanced_tts_output.wav",
                                mime="audio/wav"
                            )
                        
                        # Add to history
                        st.session_state.history.append({
                            "type": "Advanced TTS",
                            "text": text_input[:100] + "...",
                            "model": models[model_name]['name'],
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        st.error(f"Error: {result.error}")
                        
                except Exception as e:
                    st.error(f"Conversion failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_voice_clone():
    """Render Voice Cloning tab."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <strong>🎤 Voice Cloning:</strong> Upload a reference audio (5-30 seconds) of your voice,
        and the AI will clone it to speak your text with incredible accuracy.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📤 Upload Reference Voice")
        
        # File uploader with drag and drop
        uploaded_file = st.file_uploader(
            "Drag & drop your voice sample (MP3, WAV, OGG)",
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
                st.success(f"✅ Audio valid: {validation['duration']}s | {validation['sample_rate']}Hz | {validation['channels']}")
                
                # Display audio player
                st.markdown("#### 🎧 Preview Reference Voice")
                st.audio(str(temp_audio_path), format="audio/wav")
            else:
                st.error(f"❌ Invalid audio: {validation.get('message')}")
                
    with col2:
        st.markdown("### ⚙️ Voice Settings")
        
        # Language selection
        languages = VoiceClone.get_supported_languages()
        language = st.selectbox(
            "Target Language",
            options=list(languages.keys()),
            format_func=lambda x: languages[x],
            key="clone_language"
        )
        
        # Voice style/preset
        st.markdown("#### 🎭 Voice Style")
        voice_style = st.select_slider(
            "Select voice characteristics",
            options=["Neutral", "Formal", "Casual", "Emotional", "Broadcast"],
            value="Neutral"
        )
        
        # Speed control
        speed = st.slider("Speaking Speed", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
        
        # Pitch control
        pitch = st.slider("Pitch Adjustment", min_value=-12, max_value=12, value=0, step=1)
    
    st.markdown("---")
    
    # Text input section
    st.markdown("### 📝 Text to Speak")
    text_input = st.text_area(
        "Enter text for your cloned voice (max 2000 characters)",
        height=150,
        placeholder="Enter the text you want the cloned voice to speak...",
        key="clone_text",
        max_chars=2000
    )
    
    if text_input:
        char_count = len(text_input)
        st.caption(f"📊 Characters: {char_count}/2000")
        
        # Character count progress bar
        progress = min(char_count / 2000, 1.0)
        st.progress(progress)
    
    st.markdown("---")
    
    # Clone button with enhanced styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        clone_button = st.button(
            "🎵 Clone Voice & Generate Speech", 
            key="clone_voice",
            use_container_width=True
        )
    
    if clone_button:
        if not uploaded_file:
            st.error("⚠️ Please upload a reference audio file first.")
        elif not text_input.strip():
            st.error("⚠️ Please enter some text to speak.")
        else:
            # Progress message
            progress_placeholder = st.empty()
            progress_placeholder.info("🔄 Initializing voice cloning model...")
            
            try:
                # Create request
                request = VoiceCloneRequest(
                    text=text_input,
                    language=language
                )
                
                # Update progress
                progress_placeholder.info("🔄 Processing reference audio...")
                
                # Clone voice
                voice_clone = VoiceClone()
                result = voice_clone.clone_voice(
                    request=request,
                    reference_audio_path=str(temp_audio_path)
                )
                
                if result.success:
                    progress_placeholder.success("✅ Voice cloned successfully!")
                    
                    # Display results in a nice card
                    st.markdown("""
                    <div class="card">
                        <h3>🎧 Generated Audio</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display audio player
                    st.audio(result.file_path, format="audio/wav")
                    
                    # Get audio info
                    audio_info = AudioUtils.get_audio_info(result.file_path)
                    if audio_info.get("success"):
                        col_info1, col_info2, col_info3 = st.columns(3)
                        with col_info1:
                            st.metric("Duration", f"{audio_info.get('duration', 0)}s")
                        with col_info2:
                            st.metric("Sample Rate", f"{audio_info.get('sample_rate', 0)}Hz")
                        with col_info3:
                            st.metric("File Size", f"{audio_info.get('file_size_mb', 0)}MB")
                    
                    # Download button
                    with open(result.file_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Cloned Voice Audio",
                            data=f.read(),
                            file_name="cloned_voice.wav",
                            mime="audio/wav"
                        )
                    
                    # Also offer MP3 option
                    mp3_path = result.file_path.replace('.wav', '.mp3')
                    if AudioUtils.convert_format(result.file_path, mp3_path):
                        with open(mp3_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download as MP3",
                                data=f.read(),
                                file_name="cloned_voice.mp3",
                                mime="audio/mp3"
                            )
                    
                    # Add to history
                    st.session_state.history.append({
                        "type": "Voice Cloning",
                        "text": text_input[:100] + "...",
                        "language": language,
                        "style": voice_style,
                        "timestamp": datetime.now().isoformat()
                    })
                else:
                    progress_placeholder.error(f"❌ Error: {result.error}")
                    
            except Exception as e:
                progress_placeholder.error(f"❌ Voice cloning failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_history():
    """Render conversion history."""
    st.markdown("### 📜 Conversion History")
    
    if st.session_state.get('history'):
        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"{item['type']} - {item['timestamp'][:19]}"):
                st.markdown(f"**Text:** {item['text']}")
                st.markdown(f"**Type:** {item['type']}")
                st.markdown(f"**Time:** {item['timestamp'][:19]}")
    else:
        st.info("No conversions yet. Start using the TTS features!")


def main():
    """Main application function."""
    # Initialize
    SessionState.init()
    create_directories()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Main content tabs
    tabs = st.tabs([
        "🚀 Basic TTS",
        "⚡ Advanced TTS",
        "🎭 Voice Cloning",
        "📜 History"
    ])
    
    with tabs[0]:
        render_basic_tts()
    
    with tabs[1]:
        render_advanced_tts()
    
    with tabs[2]:
        render_voice_clone()
    
    with tabs[3]:
        render_history()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; padding: 1rem;'>"
        "Made with ❤️ using Streamlit | Text to Speech Pro © 2026\]"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

