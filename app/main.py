from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="DiveApp API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "✅ DiveApp API funcionando",
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/debug")
async def debug():
    """
    Debug de configuración sin imports complejos
    """
    database_url = os.getenv("DATABASE_URL", "NOT_SET")
    
    return {
        "environment": os.getenv("ENVIRONMENT", "not_set"),
        "has_database_url": bool(database_url and database_url != "NOT_SET"),
        "database_url_preview": database_url[:50] + "..." if database_url and len(database_url) > 50 else database_url,
        "python_version": "3.11.9",
        "config_status": "checking imports..."
    }

@app.get("/api/v1/test-config")
async def test_config():
    """
    Test de importación de config
    """
    try:
        from app.core.config import settings
        return {
            "message": "✅ Config importado exitosamente",
            "environment": settings.ENVIRONMENT,
            "has_database_url": bool(settings.DATABASE_URL),
            "computed_url_preview": settings.DATABASE_URL_COMPUTED[:50] + "..."
        }
    except Exception as e:
        return {
            "message": "❌ Error importando config",
            "error": str(e),
            "type": type(e).__name__
        }

@app.get("/api/v1/test-db-simple")
async def test_database_simple():
    """
    Test simple de database sin dependency injection
    """
    try:
        from app.core.config import settings
        from sqlalchemy import create_engine, text
        
        # Crear engine temporal
        engine = create_engine(settings.DATABASE_URL_COMPUTED)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            
        return {
            "message": "✅ Conexión a base de datos exitosa",
            "test_result": row[0],
            "database_url_works": True
        }
        
    except Exception as e:
        return {
            "message": "❌ Error de conexión",
            "error": str(e),
            "type": type(e).__name__
        }