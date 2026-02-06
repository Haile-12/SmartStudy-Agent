from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from pathlib import Path
from typing import Optional
import os

class Settings(BaseSettings):
    """Production configuration with validation"""
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    output_dir: Path = Field(default=Path("./outputs"), alias="OUTPUT_DIR")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    model_name: str = "gemini/gemini-2.0-flash" 
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
        populate_by_name = True

    @field_validator("output_dir", mode="before")
    @classmethod
    def resolve_path(cls, v):
        return Path(v).resolve()
    
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid:
            raise ValueError(f"Invalid log level. Must be one of {valid}")
        return v.upper()
    
    def create_dirs(self):
        """Ensure output directories exist"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "memory").mkdir(exist_ok=True)
        (self.output_dir / "materials").mkdir(exist_ok=True)
        (self.output_dir / "summaries").mkdir(exist_ok=True)

# Singleton instance
settings = Settings()
settings.create_dirs()
