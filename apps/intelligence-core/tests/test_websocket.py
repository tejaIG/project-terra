from fastapi.testclient import TestClient
from src.main import app
from src.services.event_bus import EventBus


def test_websocket_streams_events() -> None:
    bus: EventBus = app.state.event_bus
    client = TestClient(app)
    with client.websocket_connect("/ws/council/demo") as websocket:
        import asyncio

        asyncio.run(bus.publish("demo", '{"kind":"agent_thought","runId":"demo","payload":{"agentId":"quant","analysis":"ok","sentimentScore":0.1,"confidence":0.7,"createdAt":"2026-01-01T00:00:00Z"}}'))
        message = websocket.receive_text()
        assert "agent_thought" in message
