from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Create FastAPI instance
app = FastAPI(
    title="DiveApp API",
    description="API completa para la aplicación de buceo",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambiar por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import database dependencies with error handling
try:
    from sqlalchemy.orm import Session
    from app.core.database import get_db, engine
    from app.core.config import settings
    DATABASE_AVAILABLE = True
except ImportError as e:
    print(f"Database imports failed: {e}")
    DATABASE_AVAILABLE = False
    settings = None

@app.get("/")
async def root():
    """
    Endpoint básico para verificar que la API funciona
    """
    return {
        "message": "¡Bienvenido a DiveApp API!",
        "version": "1.0.0",
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "database_configured": DATABASE_AVAILABLE
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint para monitoreo
    """
    return {
        "status": "healthy",
        "database_available": DATABASE_AVAILABLE,
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/api/v1/info")
async def api_info():
    """
    Información de la API y endpoints disponibles
    """
    return {
        "api_name": "DiveApp API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "database_test": "/api/v1/test-db",
            "documentation": "/docs",
            "users": "/api/v1/users (próximamente)",
            "dive_logs": "/api/v1/dive-logs (próximamente)",
            "operators": "/api/v1/operators (próximamente)"
        },
        "database_configured": DATABASE_AVAILABLE
    }

@app.get("/api/v1/test-db")
async def test_database():
    """
    Endpoint para probar la conexión a la base de datos
    """
    # Check if database imports are available
    if not DATABASE_AVAILABLE:
        return {
            "message": "❌ Database modules not available",
            "error": "Database dependencies not imported",
            "database_url_exists": bool(os.getenv("DATABASE_URL")),
            "suggestions": [
                "Check that requirements.txt includes sqlalchemy and psycopg2-binary",
                "Verify that app/core/config.py and app/core/database.py exist",
                "Check deployment logs for import errors"
            ]
        }
    
    # Check if DATABASE_URL exists
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return {
            "message": "❌ DATABASE_URL not found",
            "error": "Environment variable DATABASE_URL is not set",
            "available_env_vars": [k for k in os.environ.keys() if 'DATA' in k.upper()]
        }
    
    # Try to connect to database
    try:
        from sqlalchemy.orm import Session
        db: Session = next(get_db())
        
        # Execute simple test query
        result = db.execute("SELECT 1 as test_value, current_timestamp as timestamp")
        row = result.fetchone()
        
        db.close()
        
        return {
            "message": "✅ Conexión a base de datos exitosa",
            "test_result": row[0],
            "timestamp": str(row[1]),
            "environment": settings.ENVIRONMENT if settings else "unknown",
            "database_url_preview": database_url[:50] + "..." if len(database_url) > 50 else database_url
        }
        
    except Exception as e:
        return {
            "message": "❌ Error conectando a la base de datos",
            "error": str(e),
            "error_type": type(e).__name__,
            "database_url_exists": True,
            "suggestions": [
                "Verify DATABASE_URL format is correct",
                "Check if PostgreSQL service is running",
                "Verify network connectivity to database"
            ]
        }

@app.get("/api/v1/test-models")
async def test_models():
    """
    Endpoint para probar que los modelos están importándose correctamente
    """
    try:
        from app.models.user import User
        from app.models.dive_log import DiveLog
        
        return {
            "message": "✅ Modelos importados correctamente",
            "models": {
                "User": str(User.__table__.columns.keys()) if hasattr(User, '__table__') else "Model defined",
                "DiveLog": str(DiveLog.__table__.columns.keys()) if hasattr(DiveLog, '__table__') else "Model defined"
            }
        }
    except ImportError as e:
        return {
            "message": "❌ Error importando modelos",
            "error": str(e),
            "suggestions": [
                "Check that app/models/user.py exists",
                "Check that app/models/dive_log.py exists", 
                "Verify __init__.py files exist in app/ and app/models/"
            ]
        }

@app.get("/api/v1/env-check")
async def environment_check():
    """
    Endpoint para verificar variables de entorno (debug)
    """
    return {
        "environment": os.getenv("ENVIRONMENT", "not_set"),
        "has_database_url": bool(os.getenv("DATABASE_URL")),
        "has_secret_key": bool(os.getenv("SECRET_KEY")),
        "python_path": os.getenv("PYTHONPATH", "not_set"),
        "available_env_vars": [k for k in os.environ.keys() if not k.startswith('_')][:20]  # Solo primeras 20
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "message": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/health", 
            "/docs",
            "/api/v1/info",
            "/api/v1/test-db",
            "/api/v1/test-models",
            "/api/v1/env-check"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "message": "Internal server error",
        "error": str(exc),
        "suggestion": "Check application logs for more details"
    }

# Solo para desarrollo local
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )