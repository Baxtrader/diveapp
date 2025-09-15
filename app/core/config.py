from typing import List, Optional
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    # App settings
    APP_NAME: str = "DiveApp API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ALGORITHM: str = "HS256"
    
    # Database - Render DATABASE_URL tiene prioridad
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Fallback database settings (para desarrollo local)
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "diveapp")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "diveapp123")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "diveapp_db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    @property
    def DATABASE_URL_COMPUTED(self) -> str:
        """
        Usar DATABASE_URL de Render si existe, sino construir desde componentes
        """
        if self.DATABASE_URL:
            # Render/Heroku style DATABASE_URL
            return self.DATABASE_URL
        
        # Construir URL para desarrollo local
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis (opcional por ahora)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # CORS origins
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        if self.ENVIRONMENT == "production":
            return [
                "https://diveapp.onrender.com",
                "https://www.diveapp.com",  # tu dominio futuro
            ]
        return [
            "http://localhost:3000",
            "http://localhost:8000",
            "http://localhost:8080",
            "http://127.0.0.1:8000",
        ]
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER: str = "uploads"
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    ALLOWED_VIDEO_EXTENSIONS: set = {".mp4", ".avi", ".mov", ".webm"}
    
    # External APIs
    MAPBOX_ACCESS_TOKEN: Optional[str] = os.getenv("MAPBOX_ACCESS_TOKEN")
    
    # Cloud storage (para el futuro)
    USE_CLOUD_STORAGE: bool = os.getenv("USE_CLOUD_STORAGE", "false").lower() == "true"
    
    # Cloudinary (para imágenes/videos)
    CLOUDINARY_URL: Optional[str] = os.getenv("CLOUDINARY_URL")
    CLOUDINARY_CLOUD_NAME: Optional[str] = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY: Optional[str] = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET: Optional[str] = os.getenv("CLOUDINARY_API_SECRET")
    
    # Email settings (para notificaciones futuras)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    
    # Debug info
    def get_debug_info(self):
        """
        Información de debug (sin datos sensibles)
        """
        return {
            "environment": self.ENVIRONMENT,
            "has_database_url": bool(self.DATABASE_URL),
            "database_url_preview": self.DATABASE_URL[:30] + "..." if self.DATABASE_URL else None,
            "postgres_server": self.POSTGRES_SERVER,
            "postgres_port": self.POSTGRES_PORT,
            "use_cloud_storage": self.USE_CLOUD_STORAGE,
            "has_secret_key": bool(self.SECRET_KEY and len(self.SECRET_KEY) > 10),
            "cors_origins_count": len(self.BACKEND_CORS_ORIGINS)
        }
    
    class Config:
        case_sensitive = True
        # No usar .env en producción - Render maneja las variables

# Crear instancia global de settings
settings = Settings()

# Para debugging - solo ejecutar si el archivo se llama directamente
if __name__ == "__main__":
    print("=== DiveApp Configuration ===")
    debug_info = settings.get_debug_info()
    for key, value in debug_info.items():
        print(f"{key}: {value}")
    
    print(f"\nComputed DATABASE_URL: {settings.DATABASE_URL_COMPUTED[:50]}...")
    print(f"CORS Origins: {settings.BACKEND_CORS_ORIGINS}")