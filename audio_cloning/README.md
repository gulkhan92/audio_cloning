# 🎤 Voice Cloning Pro

A professional-grade voice cloning web application powered by [Coqui TTS](https://github.com/coqui-ai/TTS). Transform any voice sample into natural, high-quality speech using state-of-the-art AI text-to-speech technology.

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.24%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)
![TTS](https://img.shields.io/badge/Coqui%20TTS-0.22-orange)

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 **Voice Cloning** | Clone any voice from a short audio sample (5-30 seconds) |
| 🌍 **Multi-Language** | Support for 10+ languages including English, Spanish, French, German, and more |
| 🔊 **High Quality** | Studio-quality audio output at 22kHz sample rate |
| ⚡ **Fast Processing** | Optimized for quick voice cloning and generation |
| 🔒 **Secure** | All processing done locally - your data stays private |
| 📱 **Easy UI** | Professional Streamlit interface with intuitive controls |

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- At least 4GB RAM (8GB recommended for model loading)
- ~2GB disk space for TTS models

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/gulkhan92/audio_cloning.git
cd audio_cloning
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## 📖 Usage Guide

### Basic Usage

1. **Upload Voice Sample** - Drag and drop or browse to select a clear audio recording (5-30 seconds)
2. **Select Language** - Choose the output language from the dropdown
3. **Enter Text** - Type or paste the text you want the cloned voice to speak
4. **Generate** - Click the "Clone Voice" button to generate the audio
5. **Download** - Listen to the result and download if satisfied

### Tips for Best Results

- ✅ **Do:**
  - Use clean, clear audio without background noise
  - Keep recordings between 10-30 seconds
  - Use single-speaker audio for better accuracy
  - Match the voice language to your output language

- ❌ **Don't:**
  - Use audio with multiple speakers
  - Use low-quality or noisy recordings
  - Use very short clips (under 3 seconds)
  - Expect perfect replication of emotions/intonations

## 🌐 Supported Languages

| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |
| `ja` | Japanese |
| `ko` | Korean |
| `zh` | Chinese |

## 🛠️ Tech Stack

- **Streamlit** - Modern web framework for data apps
- **Coqui TTS** - Advanced text-to-speech engine with voice cloning
- **Pydantic** - Data validation using Python type annotations
- **SoundFile** - High-performance audio file I/O
- **Librosa** - Audio and music analysis library
- **NumPy** - Numerical computing for audio processing

## 📁 Project Structure

```
audio_cloning/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md            # This file
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic validation schemas
└── utils/
    ├── __init__.py
    └── voice_clone.py   # Voice cloning logic
```

## 🔧 Configuration

### Custom Model

You can modify the voice cloning model in `utils/voice_clone.py`:

```python
self._tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/your_tts",
    progress_bar=True
)
```

### Output Directory

Default output directory is `outputs/`. To change:

```python
voice_clone = VoiceClone(output_dir="your_directory")
```

## 📝 API Reference

### VoiceCloneRequest Schema

```python
{
    "text": str,          # Required, 1-2000 characters
    "language": str        # Optional, default "en"
}
```

### TTSResponse Schema

```python
{
    "success": bool,              # Whether generation succeeded
    "message": str,               # Status message
    "file_path": Optional[str],   # Path to generated audio
    "error": Optional[str]         # Error message if failed
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Coqui AI](https://coqui.ai/) for the amazing TTS engine
- [Streamlit](https://streamlit.io/) for the web framework
- The open-source community for continuous support

## 📞 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/gulkhan92/audio_cloning/issues) page
2. Create a new issue with detailed information
3. Include error logs and steps to reproduce

---

<div align="center">

**Made with ❤️ using Coqui TTS**

[⭐ Star this repo](https://github.com/gulkhan92/audio_cloning/stargazers) • [🐛 Report Bug](https://github.com/gulkhan92/audio_cloning/issues)

</div>

