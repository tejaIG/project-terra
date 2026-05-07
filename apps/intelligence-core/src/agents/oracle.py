from ..services.event_bus import EventBus
from ..types import AgentAnalysis, AgentId, MarketData
from ..llm import get_chat_model
from ..tools import fetch_et_headlines, fetch_moneycontrol_headlines
from .base import BaseAgent


class OracleAgent(BaseAgent):
    def __init__(self, bus: EventBus) -> None:
        super().__init__(bus, AgentId.oracle)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentAnalysis:
        model = get_chat_model()
        headlines = fetch_et_headlines(ticker) + fetch_moneycontrol_headlines(ticker)
        prompt = (
            "You are Oracle sentiment agent. "
            f"Ticker: {ticker}. Headlines: {headlines}. "
            "Provide a concise sentiment summary."
        )
        result = model.invoke(prompt)
        return self._build_analysis(str(result.content), sentiment_score=0.15, confidence=0.64)
