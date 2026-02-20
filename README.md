# Text to Speech Application

## Overview
A professional Text-to-Speech web application with multiple TTS modes including basic Google TTS, advanced Coqui TTS, and voice cloning capabilities.

## Features
- **Basic TTS**: Quick text-to-speech using Google gTTS
- **Advanced TTS**: High-quality speech using Coqui TTS
- **Voice Cloning**: Clone your voice from reference audio
- **Audio Format Conversion**: Convert between MP3 and WAV formats

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

### Basic TTS
1. Enter your text in the text area
2. Select language (default: English)
3. Click "Convert to Speech" button
4. Download or play the generated audio

### Advanced TTS
1. Enter your text
2. Choose from available models
3. Click "Generate Speech"
4. Download or play the result

### Voice Cloning
1. Upload a reference audio file (5-10 seconds)
2. Enter text to speak
3. Click "Clone Voice"
4. Listen to or download the cloned voice

## Project Structure
```
Text to Speech/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── tts_basic.py      # Basic gTTS functionality
│   ├── tts_advanced.py   # Coqui TTS functionality
│   ├── voice_clone.py    # Voice cloning
│   └── audio_utils.py    # Audio conversion utilities
├── models/
│   ├── __init__.py
│   └── schemas.py        # Pydantic schemas for validation
└── README.md
```

## Dependencies
- Streamlit - Web framework
- gTTS - Google Text-to-Speech
- TTS - Coqui Text-to-Speech
- Pydantic - Data validation
- SoundFile - Audio file handling
- Librosa - Audio processing

## License
MIT License

