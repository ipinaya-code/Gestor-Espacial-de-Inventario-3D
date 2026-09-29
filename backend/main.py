from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from app.core.database import init_db
from app.presentation.routes import router as items_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa las tablas SQLite al arrancar la app
    await init_db()
    yield

app = FastAPI(
    title="3D Spatial Asset Manager API",
    description="API para la gestión de inventario e ítems en coordenadas tridimensionales (X, Y, Z)",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS para conectar sin bloqueos con el Frontend (Three.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(items_router)

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "message": "3D Spatial Asset Manager API funcionando correctamente"}

frontend_directory = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_directory, html=True), name="frontend")