import asyncio
import math
import random
from datetime import datetime, timezone
from .events import emit_price_tick
from .event_bus import EventBus
from ..types import MarketData


async def stream_ticks(bus: EventBus, run_id: str, seed: MarketData, stop_event: asyncio.Event) -> None:
    step = 0
    while not stop_event.is_set():
        drift = math.sin(step / 4.0) * 0.8
        noise = random.gauss(0, 0.25)
        price = max(1.0, seed.price + drift + noise)
        tick = MarketData(
            ticker=seed.ticker,
            price=round(price, 2),
            volume=seed.volume + (step * 100),
            commodityCorrelations=seed.commodityCorrelations,
            timestamp=datetime.now(timezone.utc),
        )
        await emit_price_tick(bus, run_id, tick)
        step += 1
        await asyncio.sleep(1)
