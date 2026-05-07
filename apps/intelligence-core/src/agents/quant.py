from ..types import AgentId, AgentResponse, MarketData
from .base import BaseAgent


class QuantAgent(BaseAgent):
    def __init__(self, bus) -> None:
        super().__init__(bus, AgentId.quant)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentResponse:
        analysis = f"{ticker}: trend and volume profile are constructive with manageable volatility."
        return self._build_response(analysis, sentiment_score=0.31, confidence=0.72)
