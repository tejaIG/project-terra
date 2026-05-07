from ..types import AgentId, AgentResponse, MarketData
from .base import BaseAgent


class GeologistAgent(BaseAgent):
    def __init__(self, bus) -> None:
        super().__init__(bus, AgentId.geologist)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentResponse:
        analysis = f"{ticker}: policy and reserves posture remains stable with long-cycle optionality."
        return self._build_response(analysis, sentiment_score=0.2, confidence=0.68)
