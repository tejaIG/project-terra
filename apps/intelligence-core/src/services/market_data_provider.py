from typing import Protocol
from ..types import MarketData


class MarketDataProvider(Protocol):
    async def next_tick(self, run_id: str, seed: MarketData) -> MarketData:
        ...
