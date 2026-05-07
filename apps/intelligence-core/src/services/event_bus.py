import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, set[asyncio.Queue[str | None]]] = {}
        self._lock = asyncio.Lock()

    async def publish(self, run_id: str, event: str | None) -> None:
        async with self._lock:
            queues = list(self._subscribers.get(run_id, set()))
        for queue in queues:
            await queue.put(event)

    @asynccontextmanager
    async def subscribe(self, run_id: str) -> AsyncIterator[AsyncIterator[str]]:
        queue: asyncio.Queue[str | None] = asyncio.Queue()
        async with self._lock:
            self._subscribers.setdefault(run_id, set()).add(queue)

        async def stream() -> AsyncIterator[str]:
            while True:
                event = await queue.get()
                if event is None:
                    return
                yield event

        try:
            yield stream()
        finally:
            async with self._lock:
                run_queues = self._subscribers.get(run_id)
                if not run_queues:
                    return
                run_queues.discard(queue)
                if not run_queues:
                    self._subscribers.pop(run_id, None)
