from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="DiveApp API",
    description="API para la aplicación de buceo",
    version="1.0.0",
)

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
        "message": "¡Bienvenido a DiveApp API!",
        "version": "1.0.0",
        "status": "running",
        "python_version": "3.11.9",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "python_version": "3.11.9"}

@app.get("/api/v1/test-db")
async def test_database_simple():
    """
    Test simple de DATABASE_URL
    """
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        return {
            "message": "✅ DATABASE_URL encontrada",
            "has_database_url": True,
            "url_preview": database_url[:30] + "..." if len(database_url) > 30 else database_url,
            "ready_for": "SQLAlchemy import en próximo deploy"
        }
    else:
        return {
            "message": "❌ DATABASE_URL no encontrada",
            "has_database_url": False,
            "note": "Agrega DATABASE_URL en Environment Variables de Render"
        }

@app.get("/api/v1/info")
async def api_info():
    """
    Información de la API
    """
    return {
        "api_name": "DiveApp API",
        "version": "1.0.0",
        "python_version": "3.11.9",
        "status": "stable",
        "endpoints": {
            "main": "/",
            "health": "/health",
            "database_test": "/api/v1/test-db",
            "documentation": "/docs",
            "info": "/api/v1/info"
        },
        "next_features": [
            "SQLAlchemy models",
            "User authentication", 
            "Dive log endpoints",
            "Operator directory"
        ]
    }