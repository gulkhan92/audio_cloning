from TTS.api import TTS
import soundfile as sf
import numpy as np

# 1. Prepare your reference audio (5-10 seconds of your voice)
reference_wav = "english.wav"  # Change this to your audio file
output_path = "cloned_output.wav"
text_to_speak = "This is my cloned voice speaking to Convert audio to right format."

# 2. Convert audio to right format (22050Hz mono)
audio, sr = sf.read(reference_wav)
if len(audio.shape) > 1: # Convert stereo to mono
    audio = np.mean(audio, axis=1)
if sr != 22050:
    from librosa import resample
    audio = resample(audio, orig_sr=sr, target_sr=22050)
sf.write("processed.wav", audio, 22050)

# 3. Load the voice cloning model
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=True)

# 4. Generate cloned voice
tts.tts_to_file(
    text=text_to_speak,
    speaker_wav="processed.wav",
    file_path=output_path,
    language="en"  # Set to your language
)

print(f"Done! Cloned voice saved to {output_path}")
