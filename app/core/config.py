from typing import List, Optional
from pydantic_settings import BaseSettings
from decouple import config

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "DiveApp API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = config("SECRET_KEY", default="your-super-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_USER: str = config("POSTGRES_USER", default="diveapp")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="diveapp123")
    POSTGRES_DB: str = config("POSTGRES_DB", default="diveapp_db")
    POSTGRES_PORT: str = config("POSTGRES_PORT", default="5432")
    
    @property
    def DATABASE_URL_COMPUTED(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://localhost:3000",
        "https://localhost:8080",
    ]
    
    # File upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif"}
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".avi", ".mov"}
    
    # External APIs
    MAPBOX_ACCESS_TOKEN: Optional[str] = config("MAPBOX_ACCESS_TOKEN", default=None)
    
    # Email settings (for future notifications)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()