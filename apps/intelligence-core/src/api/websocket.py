from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services.event_bus import EventBus

router = APIRouter(tags=["stream"])


@router.websocket("/ws/council/{run_id}")
async def stream_council(run_id: str, websocket: WebSocket) -> None:
    await websocket.accept()
    bus: EventBus = websocket.app.state.event_bus
    try:
        async with bus.subscribe(run_id) as stream:
            async for event in stream:
                await websocket.send_text(event)
    except WebSocketDisconnect:
        return
