from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create FastAPI instance
app = FastAPI(
    title="DiveApp API",
    description="API para la aplicación de buceo",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    Endpoint básico para verificar que la API funciona
    """
    return {
        "message": "¡Bienvenido a DiveApp API!",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint para monitoreo
    """
    return {"status": "healthy"}

@app.get("/api/v1/test-db")
async def test_database(db: Session = Depends(get_db)):
    """
    Endpoint para probar la conexión a la base de datos
    """
    try:
        # Ejecutar una query simple para probar la conexión
        result = db.execute("SELECT 1 as test_value")
        test_value = result.fetchone()[0]
        
        return {
            "message": "✅ Conexión a base de datos exitosa",
            "database_url": settings.DATABASE_URL_COMPUTED[:30] + "...",  # Solo mostrar inicio por seguridad
            "test_result": test_value,
            "environment": settings.ENVIRONMENT
        }
    except Exception as e:
        return {
            "message": "❌ Error conectando a la base de datos", 
            "error": str(e),
            "environment": settings.ENVIRONMENT
        }

# Solo para desarrollo local
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )