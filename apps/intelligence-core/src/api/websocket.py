from fastapi import APIRouter, WebSocket
from ..services.event_bus import EventBus

router = APIRouter(tags=["stream"])


@router.websocket("/ws/council/{run_id}")
async def stream_council(run_id: str, websocket: WebSocket) -> None:
    await websocket.accept()
    bus: EventBus = websocket.app.state.event_bus
    async for event in bus.subscribe(run_id):
        await websocket.send_text(event)
