# Audio Cloning Pro - Text to Speech

A professional voice cloning web application powered by Coqui TTS. Transform any voice sample into natural speech with AI-powered text-to-speech technology.

## Features

- 🎤 **Voice Cloning** - Clone any voice from a short audio sample
- 🌍 **Multi-Language** - Support for 10+ languages
- 🔊 **High Quality** - Studio-quality audio output
- ⚡ **Fast Processing** - Quick voice cloning
- 🔒 **Secure** - Your data stays private

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

1. **Upload Voice Sample** - Upload a clear audio recording (5-30 seconds)
2. **Enter Text** - Type the text you want the cloned voice to speak
3. **Clone Voice** - Click the button to generate

## Tips for Best Results

- Use clean, clear audio without background noise
- 10-30 seconds works best
- Single speaker audio produces better results
- The voice should be in the language you want to speak

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

## Tech Stack

- **Streamlit** - Web framework
- **Coqui TTS** - Text-to-Speech engine
- **Pydantic** - Data validation
- **SoundFile** - Audio file handling
- **Librosa** - Audio processing

## License

MIT License

