from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as analysis_router
from .api.websocket import router as websocket_router
from .config import settings
from .services.event_bus import EventBus

app = FastAPI(title="Project Terra Intelligence Core")
app.state.event_bus = EventBus()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis_router)
app.include_router(websocket_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
