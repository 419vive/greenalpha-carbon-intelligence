"""
Configuration management for GreenAlpha API
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/greenalpha"
    test_database_url: str = "postgresql://username:password@localhost:5432/greenalpha_test"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    carbon_api_key: Optional[str] = None
    sustainability_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/greenalpha.log"
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()