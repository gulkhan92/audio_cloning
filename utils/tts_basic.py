"""
Basic TTS functionality using Google gTTS.
"""
import io
import logging
from pathlib import Path
from gtts import gTTS
from models.schemas import BasicTTSRequest, TTSResponse

logger = logging.getLogger(__name__)


class BasicTTS:
    """Google gTTS text-to-speech converter."""
    
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
        'ar': 'Arabic',
        'hi': 'Hindi',
        'nl': 'Dutch',
        'pl': 'Polish',
        'tr': 'Turkish',
    }
    
    def __init__(self, output_dir: str = "outputs"):
        """Initialize BasicTTS with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert(self, request: BasicTTSRequest) -> TTSResponse:
        """
        Convert text to speech using Google gTTS.
        
        Args:
            request: BasicTTSRequest with text and options
            
        Returns:
            TTSResponse with audio file path
        """
        try:
            logger.info(f"Converting text to speech: {len(request.text)} characters")
            
            # Create gTTS object
            tts = gTTS(
                text=request.text,
                lang=request.language,
                slow=request.slow
            )
            
            # Generate filename
            output_file = self.output_dir / f"basic_tts_{self._generate_timestamp()}.mp3"
            
            # Save to file
            tts.save(str(output_file))
            
            logger.info(f"Audio saved to: {output_file}")
            
            return TTSResponse(
                success=True,
                message="Text converted to speech successfully",
                file_path=str(output_file)
            )
            
        except Exception as e:
            logger.error(f"Error in basic TTS: {str(e)}")
            return TTSResponse(
                success=False,
                message="Failed to convert text to speech",
                error=str(e)
            )
    
    def convert_to_bytes(self, request: BasicTTSRequest) -> bytes:
        """
        Convert text to speech and return as bytes.
        
        Args:
            request: BasicTTSRequest with text and options
            
        Returns:
            Audio file as bytes
        """
        try:
            tts = gTTS(
                text=request.text,
                lang=request.language,
                slow=request.slow
            )
            
            # Save to bytes buffer
            buffer = io.BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)
            
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error converting to bytes: {str(e)}")
            raise
    
    @staticmethod
    def _generate_timestamp() -> str:
        """Generate unique timestamp for filename."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @classmethod
    def get_supported_languages(cls) -> dict:
        """Get dictionary of supported languages."""
        return cls.SUPPORTED_LANGUAGES

