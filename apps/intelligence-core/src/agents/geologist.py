from ..services.event_bus import EventBus
from ..types import AgentAnalysis, AgentId, MarketData
from ..llm import get_chat_model
from ..tools import fetch_ministry_circulars, fetch_nse_announcements
from .base import BaseAgent


class GeologistAgent(BaseAgent):
    def __init__(self, bus: EventBus) -> None:
        super().__init__(bus, AgentId.geologist)

    async def analyze(self, ticker: str, market_data: MarketData) -> AgentAnalysis:
        model = get_chat_model()
        circulars = fetch_ministry_circulars(ticker)
        announcements = fetch_nse_announcements(ticker)
        prompt = (
            "You are Geologist agent for Indian mining equities. "
            f"Ticker: {ticker}. Price: {market_data.price}. "
            f"Circulars: {circulars}. Announcements: {announcements}. "
            "Give a concise fundamental analysis."
        )
        result = model.invoke(prompt)
        return self._build_analysis(str(result.content), sentiment_score=0.2, confidence=0.68)
