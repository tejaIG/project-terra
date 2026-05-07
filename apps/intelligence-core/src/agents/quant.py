from ..services.event_bus import EventBus
from ..types import AgentAnalysis, AgentId, MarketData
from ..llm import get_chat_model
from ..tools import compute_correlation, fetch_lme_spot
from .base import BaseAgent


class QuantAgent(BaseAgent):
    def __init__(self, bus: EventBus) -> None:
        super().__init__(bus, AgentId.quant)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentAnalysis:
        model = get_chat_model()
        iron_spot = fetch_lme_spot("iron_ore")
        corr = compute_correlation(ticker, "iron_ore")
        prompt = (
            "You are Quant agent. "
            f"Ticker: {ticker}. Price: {market_data.price}. Volume: {market_data.volume}. "
            f"Spot: {iron_spot}. Correlation: {corr}. "
            "Provide a concise technical and risk view."
        )
        result = model.invoke(prompt)
        return self._build_analysis(str(result.content), sentiment_score=0.31, confidence=0.72)
