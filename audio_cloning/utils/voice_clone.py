"""
Voice cloning functionality using Coqui TTS.
"""
import logging
import numpy as np
import soundfile as sf
from pathlib import Path
from TTS.api import TTS
from models.schemas import VoiceCloneRequest, TTSResponse

logger = logging.getLogger(__name__)


class VoiceClone:
    """Voice cloning using Coqui TTS."""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
    }
    
    def __init__(self, output_dir: str = "outputs", temp_dir: str = "temp"):
        """Initialize VoiceClone with output and temp directories."""
        self.output_dir = Path(output_dir)
        self.temp_dir = Path(temp_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self._tts = None
    
    @property
    def tts(self) -> TTS:
        """Lazy loading of TTS model."""
        if self._tts is None:
            logger.info("Loading voice cloning model...")
            self._tts = TTS(
                model_name="tts_models/multilingual/multi-dataset/your_tts",
                progress_bar=True
            )
            logger.info("Voice cloning model loaded successfully")
        return self._tts
    
    def clone_voice(
        self,
        request: VoiceCloneRequest,
        reference_audio_path: str
    ) -> TTSResponse:
        """
        Clone voice from reference audio and speak given text.
        
        Args:
            request: VoiceCloneRequest with text and language
            reference_audio_path: Path to reference audio file
            
        Returns:
            TTSResponse with audio file path
        """
        try:
            logger.info(f"Cloning voice: {len(request.text)} characters")
            
            # Process reference audio
            processed_audio_path = self._process_reference_audio(reference_audio_path)
            
            if processed_audio_path is None:
                return TTSResponse(
                    success=False,
                    message="Failed to process reference audio",
                    error="Could not process the audio file. Please ensure it's a valid audio file (5-10 seconds)."
                )
            
            # Generate filename
            output_file = self.output_dir / f"cloned_voice_{self._generate_timestamp()}.wav"
            
            # Generate cloned voice
            self.tts.tts_to_file(
                text=request.text,
                speaker_wav=str(processed_audio_path),
                file_path=str(output_file),
                language=request.language
            )
            
            logger.info(f"Cloned voice saved to: {output_file}")
            
            return TTSResponse(
                success=True,
                message="Voice cloned successfully",
                file_path=str(output_file)
            )
            
        except Exception as e:
            logger.error(f"Error in voice cloning: {str(e)}")
            return TTSResponse(
                success=False,
                message="Failed to clone voice",
                error=str(e)
            )
    
    def _process_reference_audio(self, audio_path: str) -> Path:
        """
        Process reference audio to required format (22050Hz mono).
        
        Args:
            audio_path: Path to reference audio file
            
        Returns:
            Path to processed audio file
        """
        try:
            import librosa
            
            # Read audio file
            audio, sr = sf.read(audio_path)
            
            # Convert stereo to mono if needed
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)
            
            # Resample to 22050Hz if needed
            if sr != 22050:
                audio = librosa.resample(audio, orig_sr=sr, target_sr=22050)
            
            # Save processed audio
            processed_path = self.temp_dir / f"processed_ref_{self._generate_timestamp()}.wav"
            sf.write(str(processed_path), audio, 22050)
            
            logger.info(f"Reference audio processed: {processed_path}")
            return processed_path
            
        except Exception as e:
            logger.error(f"Error processing reference audio: {str(e)}")
            return None
    
    def validate_reference_audio(self, audio_path: str) -> dict:
        """
        Validate reference audio file.
        
        Args:
            audio_path: Path to reference audio file
            
        Returns:
            Dictionary with validation results
        """
        try:
            audio, sr = sf.read(audio_path)
            duration = len(audio) / sr if sr else 0
            
            # Convert stereo to mono for duration calculation
            if len(audio.shape) > 1:
                audio = np.mean(audio, axis=1)
            
            # Check duration
            is_valid_duration = 3 <= duration <= 30
            
            return {
                "valid": True,
                "duration": round(duration, 2),
                "sample_rate": sr,
                "channels": "stereo" if len(audio.shape) > 1 else "mono",
                "message": "Audio is valid" if is_valid_duration else "Audio duration should be between 3-30 seconds"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "message": "Could not read audio file"
            }
    
    @staticmethod
    def _generate_timestamp() -> str:
        """Generate unique timestamp for filename."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @classmethod
    def get_supported_languages(cls) -> dict:
        """Get dictionary of supported languages."""
        return cls.SUPPORTED_LANGUAGES

