"""
Advanced TTS functionality using Coqui TTS.
"""
import logging
from pathlib import Path
from TTS.api import TTS
from models.schemas import AdvancedTTSRequest, TTSResponse

logger = logging.getLogger(__name__)


class AdvancedTTS:
    """Coqui TTS text-to-speech converter."""
    
    AVAILABLE_MODELS = {
        "tts_models/en/ljspeech/tacotron2-DDC": {
            "name": "Tacotron2 DDC",
            "description": "High quality English TTS model",
            "languages": ["en"]
        },
        "tts_models/en/ljspeech/glow-tts": {
            "name": "Glow-TTS",
            "description": "Fast English TTS model",
            "languages": ["en"]
        },
        "tts_models/multilingual/multi-dataset/your_tts": {
            "name": "YourTTS",
            "description": "Multilingual TTS with voice cloning support",
            "languages": ["en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]
        },
    }
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize AdvancedTTS with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._tts = None
    
    @property
    def tts(self) -> TTS:
        """Lazy loading of TTS model."""
        if self._tts is None:
            logger.info("Loading Coqui TTS model...")
            self._tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=True)
            logger.info("Model loaded successfully")
        return self._tts
    
    def convert(self, request: AdvancedTTSRequest) -> TTSResponse:
        """
        Convert text to speech using Coqui TTS.
        
        Args:
            request: AdvancedTTSRequest with text and model options
            
        Returns:
            TTSResponse with audio file path
        """
        try:
            logger.info(f"Converting text with advanced TTS: {len(request.text)} characters")
            
            # Generate filename
            output_file = self.output_dir / f"advanced_tts_{self._generate_timestamp()}.wav"
            
            # Load model if different from current
            if self._tts is None or getattr(self._tts, 'model_name', None) != request.model_name:
                logger.info(f"Loading model: {request.model_name}")
                self._tts = TTS(model_name=request.model_name, progress_bar=True)
            
            # Generate speech
            self.tts.tts_to_file(
                text=request.text,
                file_path=str(output_file)
            )
            
            logger.info(f"Audio saved to: {output_file}")
            
            return TTSResponse(
                success=True,
                message="Text converted to speech successfully",
                file_path=str(output_file)
            )
            
        except Exception as e:
            logger.error(f"Error in advanced TTS: {str(e)}")
            return TTSResponse(
                success=False,
                message="Failed to convert text to speech",
                error=str(e)
            )
    
    def convert_multilingual(self, text: str, language: str = "en") -> TTSResponse:
        """
        Convert text to speech using multilingual model.
        
        Args:
            text: Text to convert
            language: Language code
            
        Returns:
            TTSResponse with audio file path
        """
        try:
            logger.info(f"Converting multilingual text: {len(text)} characters in {language}")
            
            # Generate filename
            output_file = self.output_dir / f"multilingual_tts_{self._generate_timestamp()}.wav"
            
            # Load multilingual model
            model_name = "tts_models/multilingual/multi-dataset/your_tts"
            if self._tts is None or getattr(self._tts, 'model_name', None) != model_name:
                logger.info(f"Loading multilingual model: {model_name}")
                self._tts = TTS(model_name=model_name, progress_bar=True)
            
            # Generate speech
            self.tts.tts_to_file(
                text=text,
                file_path=str(output_file),
                language=language
            )
            
            logger.info(f"Audio saved to: {output_file}")
            
            return TTSResponse(
                success=True,
                message="Text converted to speech successfully",
                file_path=str(output_file)
            )
            
        except Exception as e:
            logger.error(f"Error in multilingual TTS: {str(e)}")
            return TTSResponse(
                success=False,
                message="Failed to convert text to speech",
                error=str(e)
            )
    
    @staticmethod
    def _generate_timestamp() -> str:
        """Generate unique timestamp for filename."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @classmethod
    def get_available_models(cls) -> dict:
        """Get dictionary of available models."""
        return cls.AVAILABLE_MODELS

