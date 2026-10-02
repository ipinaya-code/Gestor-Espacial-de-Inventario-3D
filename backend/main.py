import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = Path(__file__).resolve().parent
for extra_path in (str(PROJECT_ROOT), str(BACKEND_ROOT)):
    if extra_path not in sys.path:
        sys.path.insert(0, extra_path)

try:
    from app.core.database import init_db
    from app.presentation.routes import router as items_router
except ModuleNotFoundError:
    try:
        from backend.app.core.database import init_db
        from backend.app.presentation.routes import router as items_router
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "No se pudo importar el backend. Inicia Uvicorn desde la raíz del proyecto o asegura que la carpeta backend esté en PYTHONPATH."
        ) from exc

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