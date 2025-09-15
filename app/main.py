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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)