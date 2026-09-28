from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .database import engine, Base
from .api.endpoints import router as api_router
from .realtime.websocket_manager import ws_manager
from .realtime.scheduler import background_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

# Initialize database schema
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch background scheduler
    logger.info("Initializing Real-Time Brand Monitoring Application...")
    background_scheduler.start()
    yield
    # Shutdown: stop background scheduler
    logger.info("Shutting down Real-Time Brand Monitoring Application...")
    background_scheduler.stop()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

# WebSocket endpoint for real-time brand telemetry
@app.websocket("/ws/brand/{brand_id}")
async def websocket_brand_endpoint(websocket: WebSocket, brand_id: int):
    await ws_manager.connect(brand_id, websocket)
    try:
        while True:
            # Keep socket alive and receive incoming ping messages if any
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(brand_id, websocket)
    except Exception as e:
        logger.warning(f"WebSocket exception: {e}")
        ws_manager.disconnect(brand_id, websocket)
