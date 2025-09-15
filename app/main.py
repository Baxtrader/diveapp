from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
import uvicorn

app = FastAPI(
    title="DiveApp API",
    description="API completa para la aplicación de buceo",
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
        "environment": settings.ENVIRONMENT,
        "database_configured": True
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "python_version": "3.11.9",
        "environment": settings.ENVIRONMENT
    }

@app.get("/api/v1/test-db")
async def test_database(db: Session = Depends(get_db)):
    """
    Test real de conexión a PostgreSQL
    """
    try:
        # Ejecutar query real para probar conexión (SQLAlchemy 2.0 syntax)
        result = db.execute(text("SELECT 1 as test_value, current_timestamp as timestamp, version() as db_version"))
        row = result.fetchone()
        
        return {
            "message": "✅ Conexión a base de datos exitosa",
            "test_result": row[0],
            "timestamp": str(row[1]),
            "database_version": row[2][:50] + "..." if len(row[2]) > 50 else row[2],
            "environment": settings.ENVIRONMENT,
            "ready_for": "Crear tablas y endpoints"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "❌ Error conectando a la base de datos",
                "error": str(e),
                "type": type(e).__name__
            }
        )

@app.get("/api/v1/info")
async def api_info():
    """
    Información completa de la API
    """
    return {
        "api_name": "DiveApp API",
        "version": "1.0.0",
        "python_version": "3.11.9",
        "environment": settings.ENVIRONMENT,
        "status": "production_ready",
        "features": {
            "database": "PostgreSQL with PostGIS",
            "authentication": "JWT tokens",
            "validation": "Pydantic v2"
        },
        "endpoints": {
            "health": "/health",
            "database_test": "/api/v1/test-db",
            "documentation": "/docs",
            "api_info": "/api/v1/info"
        },
        "coming_soon": [
            "/api/v1/auth/register - Registro de usuarios",
            "/api/v1/auth/login - Login",
            "/api/v1/users/me - Perfil de usuario",
            "/api/v1/dive-logs - CRUD de registros de buceo",
            "/api/v1/operators - Directorio de operadores"
        ]
    }

# Solo para desarrollo local
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )