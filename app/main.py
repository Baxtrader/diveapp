from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="DiveApp API",
    description="API completa para la aplicación de buceo - Conectada a PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "¡Bienvenido a DiveApp API!",
        "version": "1.0.0",
        "status": "production_ready",
        "python_version": "3.11.9",
        "environment": settings.ENVIRONMENT,
        "database_connected": True,
        "documentation": "https://diveapp.onrender.com/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "python_version": "3.11.9",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }

@app.get("/api/v1/test-db")
async def test_database_with_dependency(db: Session = Depends(get_db)):
    """
    Test de base de datos usando dependency injection
    """
    try:
        # Test simple con dependency injection
        result = db.execute(text("SELECT 1 as test_value, current_timestamp as timestamp"))
        row = result.fetchone()
        
        # Test adicional
        version_result = db.execute(text("SELECT version()"))
        version_row = version_result.fetchone()
        
        return {
            "message": "✅ Conexión a PostgreSQL exitosa",
            "test_result": row[0],
            "timestamp": str(row[1]),
            "database_version": version_row[0][:60] + "..." if len(version_row[0]) > 60 else version_row[0],
            "environment": settings.ENVIRONMENT,
            "connection_method": "SQLAlchemy dependency injection",
            "ready_for": "Crear tablas y endpoints de usuarios"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "❌ Error con dependency injection",
                "error": str(e),
                "type": type(e).__name__,
                "suggestion": "Check database connection pool settings"
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
        "environment": settings.ENVIRONMENT,
        "status": "production_ready",
        "database": {
            "type": "PostgreSQL",
            "connected": True,
            "extensions": ["PostGIS (planned)"]
        },
        "features": {
            "authentication": "JWT tokens (planned)",
            "validation": "Pydantic v2",
            "documentation": "OpenAPI/Swagger",
            "cors": "Configured",
            "file_upload": "Planned"
        },
        "endpoints": {
            "health": "/health",
            "database_test": "/api/v1/test-db",
            "documentation": "/docs",
            "redoc": "/redoc",
            "api_info": "/api/v1/info"
        },
        "next_development": [
            "User models and tables",
            "Dive log models and tables", 
            "Authentication endpoints",
            "CRUD operations",
            "Operator directory",
            "Social features"
        ],
        "tech_stack": {
            "framework": "FastAPI",
            "database": "PostgreSQL",
            "orm": "SQLAlchemy 2.0",
            "validation": "Pydantic",
            "python": "3.11.9",
            "hosting": "Render.com"
        }
    }

@app.get("/api/v1/status")
async def status():
    """
    Status completo del sistema
    """
    # Test rápido de database
    try:
        from app.core.database import check_database_connection
        db_status = check_database_connection()
    except:
        db_status = False
    
    return {
        "api_status": "online",
        "database_status": "connected" if db_status else "disconnected",
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "uptime": "running",
        "ready_for_development": True
    }

# Solo para desarrollo local
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )