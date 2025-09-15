from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings

# Create FastAPI instance
app = FastAPI(
    title="DiveApp API",
    description="API para buceo - Sin geoalchemy2",
    version="1.0.0",
)

# Add CORS middleware
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
        "message": "DiveApp API funcionando sin geoalchemy2",
        "version": "1.0.0",
        "status": "simplified_version"
    }

@app.get("/api/v1/test-db")
async def test_database_working(db: Session = Depends(get_db)):
    """
    Test de base de datos funcionando
    """
    try:
        result = db.execute(text("SELECT 1 as test_value, current_timestamp as timestamp"))
        row = result.fetchone()
        
        return {
            "message": "✅ Base de datos funcionando perfectamente",
            "test_result": row[0],
            "timestamp": str(row[1]),
            "ready_for": "Crear endpoints reales sin geografía por ahora"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "❌ Error de base de datos",
                "error": str(e)
            }
        )

@app.get("/api/v1/test-models")
async def test_models_simple():
    """Test de modelos sin geoalchemy2"""
    try:
        from app.models.user import User
        from app.models.dive_log import DiveLog
        
        return {
            "message": "✅ Modelos funcionando",
            "user_model": "OK",
            "dive_log_model": "OK (sin Geography)",
            "next_step": "Agregar endpoints básicos"
        }
        
    except Exception as e:
        return {
            "message": "❌ Error en modelos",
            "error": str(e)
        }