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

@app.get("/health")
async def health():
    return {"status": "healthy"}

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

@app.get("/api/v1/recreate-tables")
async def recreate_tables():
    """
    Recrear tablas sin geoalchemy2 - EJECUTAR UNA SOLA VEZ
    """
    try:
        from app.models.user import User
        from app.models.dive_log import DiveLog
        from app.core.database import Base, engine
        
        # Eliminar tablas existentes
        Base.metadata.drop_all(bind=engine)
        
        # Crear tablas nuevas
        Base.metadata.create_all(bind=engine)
        
        # Verificar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        return {
            "message": "✅ Tablas recreadas exitosamente",
            "tables_created": tables,
            "user_model": "OK",
            "dive_log_model": "OK (con lat/lng en lugar de Geography)",
            "next_step": "Agregar endpoints de registro y login"
        }
        
    except Exception as e:
        return {
            "message": "❌ Error recreando tablas",
            "error": str(e),
            "type": type(e).__name__
        }

@app.post("/api/v1/register")
async def register_user_simple(
    email: str,
    username: str,
    password: str,
    full_name: str = None,
    db: Session = Depends(get_db)
):
    """
    Registro básico de usuario (sin validación compleja por ahora)
    """
    try:
        from app.models.user import User
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Verificar si email ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Verificar si username ya existe
        existing_username = db.query(User).filter(User.username == username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Crear usuario
        hashed_password = pwd_context.hash(password)
        
        new_user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "message": "✅ Usuario registrado exitosamente",
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "created_at": str(new_user.created_at)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@app.post("/api/v1/login")
async def login_user_simple(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    Login básico de usuario
    """
    try:
        from app.models.user import User
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Buscar usuario
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verificar password
        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Actualizar last_login
        from datetime import datetime
        user.last_login = datetime.utcnow()
        db.commit()
        
        return {
            "message": "✅ Login exitoso",
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "last_login": str(user.last_login),
            "total_dives": user.total_dives
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.post("/api/v1/dive-logs")
async def create_dive_log(
    user_id: int,
    dive_site_name: str,
    max_depth: float,
    dive_date: str,  # formato: "2025-01-15T10:00:00"
    country: str = None,
    notes: str = None,
    dive_duration: int = None,  # en minutos
    water_temperature: float = None,
    visibility: float = None,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo registro de buceo
    """
    try:
        from app.models.dive_log import DiveLog
        from app.models.user import User
        from datetime import datetime
        
        # Verificar que el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calcular siguiente dive number
        last_dive = db.query(DiveLog).filter(DiveLog.user_id == user_id).order_by(DiveLog.dive_number.desc()).first()
        next_dive_number = 1 if not last_dive else last_dive.dive_number + 1
        
        # Parsear fecha
        dive_datetime = datetime.fromisoformat(dive_date.replace('Z', '+00:00'))
        
        # Crear dive log
        new_dive = DiveLog(
            user_id=user_id,
            dive_number=next_dive_number,
            dive_site_name=dive_site_name,
            dive_date=dive_datetime,
            max_depth=max_depth,
            country=country,
            notes=notes,
            dive_duration=dive_duration,
            water_temperature=water_temperature,
            visibility=visibility
        )
        
        db.add(new_dive)
        db.commit()
        db.refresh(new_dive)
        
        # Actualizar total_dives del usuario
        user.total_dives = next_dive_number
        if max_depth and (not user.max_depth_achieved or max_depth > user.max_depth_achieved):
            user.max_depth_achieved = max_depth
        db.commit()
        
        return {
            "message": "✅ Dive log creado exitosamente",
            "dive_id": new_dive.id,
            "dive_number": new_dive.dive_number,
            "dive_site": new_dive.dive_site_name,
            "max_depth": new_dive.max_depth,
            "user_total_dives": user.total_dives,
            "created_at": str(new_dive.created_at)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating dive log: {str(e)}")

@app.get("/api/v1/dive-logs/{user_id}")
async def get_user_dive_logs(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los dive logs de un usuario
    """
    try:
        from app.models.dive_log import DiveLog
        from app.models.user import User
        
        # Verificar usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Obtener dive logs
        dive_logs = db.query(DiveLog).filter(DiveLog.user_id == user_id).order_by(DiveLog.dive_date.desc()).all()
        
        return {
            "message": "✅ Dive logs obtenidos",
            "user": {
                "id": user.id,
                "username": user.username,
                "total_dives": user.total_dives,
                "max_depth_achieved": user.max_depth_achieved
            },
            "dive_logs": [
                {
                    "id": dive.id,
                    "dive_number": dive.dive_number,
                    "dive_site_name": dive.dive_site_name,
                    "dive_date": str(dive.dive_date),
                    "max_depth": dive.max_depth,
                    "country": dive.country,
                    "notes": dive.notes,
                    "dive_duration": dive.dive_duration,
                    "water_temperature": dive.water_temperature,
                    "visibility": dive.visibility
                }
                for dive in dive_logs
            ],
            "total_dives_count": len(dive_logs)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dive logs: {str(e)}")
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)