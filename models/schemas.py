"""
Pydantic schemas for data validation in the TTS application.
"""
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re


class BasicTTSRequest(BaseModel):
    """Schema for Basic TTS request validation."""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    language: str = Field(default="en", description="Language code (e.g., 'en', 'es', 'fr')")
    slow: bool = Field(default=False, description="Whether to use slow speech rate")
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v: str) -> str:
        supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi', 'nl', 'pl', 'tr']
        if v not in supported_languages:
            raise ValueError(f"Language '{v}' not supported. Choose from: {', '.join(supported_languages)}")
        return v


class AdvancedTTSRequest(BaseModel):
    """Schema for Advanced TTS request validation."""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    model_name: str = Field(default="tts_models/en/ljspeech/tacotron2-DDC", description="TTS model name")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()


class VoiceCloneRequest(BaseModel):
    """Schema for Voice Cloning request validation."""
    text: str = Field(..., min_length=1, max_length=2000, description="Text to speak")
    language: str = Field(default="en", description="Language code")
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v.strip()
    
    @field_validator('language')
    @classmethod
    def validate_language(cls, v: str) -> str:
        supported_languages = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh']
        if v not in supported_languages:
            raise ValueError(f"Language '{v}' not supported")
        return v


class AudioConversionRequest(BaseModel):
    """Schema for audio conversion request validation."""
    input_format: str = Field(..., description="Input audio format (mp3, wav, etc.)")
    output_format: str = Field(..., description="Output audio format")
    
    @field_validator('input_format', 'output_format')
    @classmethod
    def validate_format(cls, v: str) -> str:
        supported_formats = ['mp3', 'wav', 'ogg', 'flac', 'm4a']
        if v.lower() not in supported_formats:
            raise ValueError(f"Format '{v}' not supported. Choose from: {', '.join(supported_formats)}")
        return v.lower()


class TTSResponse(BaseModel):
    """Schema for TTS response."""
    success: bool
    message: str
    file_path: Optional[str] = None
    audio_data: Optional[bytes] = None
    error: Optional[str] = None


class AppConfig(BaseModel):
    """Application configuration schema."""
    app_name: str = Field(default="Text to Speech Pro")
    app_description: str = Field(default="Professional Text-to-Speech Converter")
    max_text_length: int = Field(default=5000)
    supported_languages: List[str] = Field(default_factory=lambda: [
        'en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi', 'nl', 'pl', 'tr'
    ])
    output_directory: str = Field(default="outputs")
    temp_directory: str = Field(default="temp")

