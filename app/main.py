from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Create FastAPI instance
app = FastAPI(
    title="DiveApp API",
    description="API para la aplicación de buceo",
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
    """
    Endpoint básico para verificar que la API funciona
    """
    return {
        "message": "¡Bienvenido a DiveApp API!",
        "version": "1.0.1",
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "deploy_test": "forced_deploy"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint para monitoreo
    """
    return {"status": "healthy"}

@app.get("/api/v1/test")
async def test_endpoint():
    """
    Endpoint de prueba simple
    """
    return {
        "message": "API v1 funcionando correctamente",
        "database_url_exists": bool(os.getenv("DATABASE_URL")),
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Solo para desarrollo local
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )