from ..types import AgentId, AgentResponse, MarketData
from .base import BaseAgent


class OracleAgent(BaseAgent):
    def __init__(self, bus) -> None:
        super().__init__(bus, AgentId.oracle)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentResponse:
        analysis = f"{ticker}: sentiment pulse is mildly positive with no panic signals."
        return self._build_response(analysis, sentiment_score=0.15, confidence=0.64)
