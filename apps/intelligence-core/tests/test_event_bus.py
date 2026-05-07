import asyncio
from src.services.event_bus import EventBus


async def _collect_one(bus: EventBus, run_id: str) -> str:
    async with bus.subscribe(run_id) as stream:
        async for event in stream:
            return event
    return ""


def test_event_bus_fanout() -> None:
    async def run() -> None:
        bus = EventBus()
        task_a = asyncio.create_task(_collect_one(bus, "run-1"))
        task_b = asyncio.create_task(_collect_one(bus, "run-1"))
        await asyncio.sleep(0)
        await bus.publish("run-1", "hello")
        await bus.publish("run-1", None)
        assert await task_a == "hello"
        assert await task_b == "hello"

    asyncio.run(run())
