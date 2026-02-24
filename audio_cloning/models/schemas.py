"""
Pydantic schemas for data validation in the Voice Cloning application.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class VoiceCloneRequest(BaseModel):
    """Schema for Voice Cloning request."""
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


class TTSResponse(BaseModel):
    """Schema for TTS response."""
    success: bool
    message: str
    file_path: Optional[str] = None
    audio_data: Optional[bytes] = None
    error: Optional[str] = None

