from ..services.event_bus import EventBus
from ..types import AgentAnalysis, AgentId, MarketData, RiskParams, TradeAction, TradeSignal
from ..llm import get_chat_model
from .base import BaseAgent


class StrategistAgent(BaseAgent):
    def __init__(self, bus: EventBus) -> None:
        super().__init__(bus, AgentId.strategist)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentAnalysis:
        model = get_chat_model()
        prompt = (
            "You are Lead Strategist agent. "
            f"Ticker: {ticker}. Latest price: {market_data.price}. "
            "Synthesize prior agent viewpoints into a tactical signal rationale."
        )
        result = model.invoke(prompt)
        return self._build_analysis(str(result.content), sentiment_score=0.28, confidence=0.82)

    def to_signal(self, ticker: str) -> TradeSignal:
        return TradeSignal(
            ticker=ticker,
            action=TradeAction.BUY,
            rationale="Council consensus is positive with acceptable risk envelope.",
            riskParams=RiskParams(stopLossPct=2.0, takeProfitPct=4.5, maxPositionSizePct=5.0),
        )
