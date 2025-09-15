from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine con configuración para producción
engine = create_engine(
    settings.DATABASE_URL_COMPUTED,
    pool_pre_ping=True,  # Verificar conexiones antes de usar
    pool_recycle=300,    # Reciclar conexiones cada 5 minutos
    pool_size=5,         # Máximo 5 conexiones simultáneas
    max_overflow=0,      # No permitir conexiones adicionales
    echo=False,          # Set to True para ver SQL queries en logs
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for declarative models
Base = declarative_base()

# Dependency para obtener sesión de base de datos
def get_db():
    """
    Dependency que provee una sesión de base de datos
    Se cierra automáticamente después de cada request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para verificar conexión de base de datos
def check_database_connection():
    """
    Verificar que la conexión a la base de datos funciona
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Función para crear todas las tablas
def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

# Para debugging
if __name__ == "__main__":
    print("=== Database Configuration ===")
    print(f"Database URL: {settings.DATABASE_URL_COMPUTED[:50]}...")
    print(f"Testing connection...")
    
    if check_database_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")