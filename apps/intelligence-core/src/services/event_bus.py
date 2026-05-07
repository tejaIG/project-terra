import asyncio
from collections import defaultdict
from typing import AsyncIterator


class EventBus:
    def __init__(self) -> None:
        self._queues: defaultdict[str, asyncio.Queue[str]] = defaultdict(asyncio.Queue)

    async def publish(self, run_id: str, event: str) -> None:
        await self._queues[run_id].put(event)

    async def subscribe(self, run_id: str) -> AsyncIterator[str]:
        queue = self._queues[run_id]
        while True:
            yield await queue.get()
