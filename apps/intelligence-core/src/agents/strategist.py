from ..types import AgentId, AgentResponse, MarketData, TradeSignal, TradeAction, RiskParams
from .base import BaseAgent


class StrategistAgent(BaseAgent):
    def __init__(self, bus) -> None:
        super().__init__(bus, AgentId.strategist)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentResponse:
        analysis = f"{ticker}: consensus leans tactical long with strict downside controls."
        return self._build_response(analysis, sentiment_score=0.28, confidence=0.7)

    def to_signal(self, ticker: str) -> TradeSignal:
        return TradeSignal(
            ticker=ticker,
            action=TradeAction.BUY,
            rationale="Council consensus is positive with acceptable risk envelope.",
            riskParams=RiskParams(stopLossPct=2.0, takeProfitPct=4.5, maxPositionSizePct=5.0),
        )
