from pydub import AudioSegment

# Ensure ffmpeg is available
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"  # adjust path if needed

# Load the .mp3 file (replace with your actual path)
mp3_path = "audio.mp3"
wav_path = "output.wav"

try:
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    audio.export(wav_path, format="wav")
    print("Conversion successful.")
except Exception as e:
    print("Error during conversion:", e)
