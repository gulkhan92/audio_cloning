"""
Audio utility functions for format conversion and processing.
"""
import logging
import io
from pathlib import Path
from typing import Optional, Tuple
import numpy as np
import soundfile as sf
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioUtils:
    """Audio format conversion and processing utilities."""
    
    SUPPORTED_FORMATS = ['mp3', 'wav', 'ogg', 'flac', 'm4a']
    
    @staticmethod
    def convert_format(
        input_path: str,
        output_path: str,
        format: Optional[str] = None
    ) -> bool:
        """
        Convert audio file from one format to another.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to output audio file
            format: Output format (if not inferred from output_path)
            
        Returns:
            True if conversion successful, False otherwise
        """
        try:
            # Determine format from extension if not provided
            if format is None:
                format = Path(output_path).suffix[1:].lower()
            
            # Load audio
            audio = AudioSegment.from_file(input_path)
            
            # Export in new format
            audio.export(output_path, format=format)
            
            logger.info(f"Converted {input_path} to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error converting audio: {str(e)}")
            return False
    
    @staticmethod
    def mp3_to_wav(input_path: str, output_path: str) -> bool:
        """Convert MP3 to WAV format."""
        return AudioUtils.convert_format(input_path, output_path, 'wav')
    
    @staticmethod
    def wav_to_mp3(input_path: str, output_path: str, bitrate: str = "192k") -> bool:
        """Convert WAV to MP3 format."""
        try:
            audio = AudioSegment.from_wav(input_path)
            audio.export(output_path, format="mp3", bitrate=bitrate)
            logger.info(f"Converted {input_path} to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error converting to MP3: {str(e)}")
            return False
    
    @staticmethod
    def get_audio_info(audio_path: str) -> dict:
        """
        Get information about an audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with audio information
        """
        try:
            audio, sr = sf.read(audio_path)
            
            # Get duration
            duration = len(audio) / sr
            
            # Get channels
            channels = 1 if len(audio.shape) == 1 else audio.shape[1]
            
            # Get file size
            file_size = Path(audio_path).stat().st_size
            
            return {
                "success": True,
                "sample_rate": sr,
                "channels": channels,
                "duration": round(duration, 2),
                "file_size": file_size,
                "file_size_mb": round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting audio info: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def normalize_audio(audio_path: str, output_path: str) -> bool:
        """
        Normalize audio file.
        
        Args:
            audio_path: Path to input audio file
            output_path: Path to output normalized audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            audio, sr = sf.read(audio_path)
            
            # Normalize to -1dBFS
            peak = np.abs(audio).max()
            if peak > 0:
                target_peak = 0.9  # -1dBFS
                audio = audio * (target_peak / peak)
            
            sf.write(output_path, audio, sr)
            logger.info(f"Normalized audio saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error normalizing audio: {str(e)}")
            return False
    
    @staticmethod
    def trim_silence(
        audio_path: str,
        output_path: str,
        silence_thresh: float = 0.01,
        min_silence_len: int = 500
    ) -> bool:
        """
        Trim silence from audio file.
        
        Args:
            audio_path: Path to input audio file
            output_path: Path to output trimmed audio
            silence_thresh: Silence threshold (0-1)
            min_silence_len: Minimum silence length in ms
            
        Returns:
            True if successful, False otherwise
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            
            # Trim silence from start and end
            trimmed = audio.strip_silence(
                silence_thresh=silence_thresh,
                min_silence_len=min_silence_len
            )
            
            trimmed.export(output_path, format=Path(output_path).suffix[1:])
            logger.info(f"Trimmed audio saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error trimming silence: {str(e)}")
            return False
    
    @staticmethod
    def merge_audio(audio_files: list, output_path: str) -> bool:
        """
        Merge multiple audio files into one.
        
        Args:
            audio_files: List of audio file paths
            output_path: Path to output merged audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            combined = AudioSegment.empty()
            
            for audio_file in audio_files:
                audio = AudioSegment.from_file(audio_file)
                combined += audio
            
            combined.export(output_path, format=Path(output_path).suffix[1:])
            logger.info(f"Merged audio saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error merging audio: {str(e)}")
            return False
    
    @staticmethod
    def change_volume(audio_path: str, output_path: str, volume_db: float) -> bool:
        """
        Change audio volume.
        
        Args:
            audio_path: Path to input audio file
            output_path: Path to output audio
            volume_db: Volume change in dB
            
        Returns:
            True if successful, False otherwise
        """
        try:
            audio = AudioSegment.from_file(audio_path)
            adjusted = audio + volume_db
            adjusted.export(output_path, format=Path(output_path).suffix[1:])
            logger.info(f"Volume adjusted audio saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error changing volume: {str(e)}")
            return False

