from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any
from ..types import AgentAnalysis, AgentId, MarketData
from ..services.event_bus import EventBus
from ..services.events import emit_agent_thought
from ..services.persistence import save_agent_analysis


class BaseAgent(ABC):
    def __init__(self, bus: EventBus, agent_id: AgentId) -> None:
        self.bus = bus
        self.agent_id = agent_id

    @abstractmethod
    async def analyze(self, ticker: str, market_data: MarketData) -> AgentAnalysis:
        raise NotImplementedError

    async def _emit(self, run_id: str, ticker: str, analysis: AgentAnalysis) -> None:
        await emit_agent_thought(self.bus, run_id, analysis)
        await save_agent_analysis(run_id=run_id, ticker=ticker, analysis=analysis)

    async def run_node(self, state: dict[str, Any]) -> dict[str, Any]:
        analysis = await self.analyze(state["ticker"], state["market_data"])
        await self._emit(state["run_id"], state["ticker"], analysis)
        state[self.agent_id.value] = analysis
        return state

    def _build_analysis(self, analysis: str, sentiment_score: float, confidence: float) -> AgentAnalysis:
        return AgentAnalysis(
            agentId=self.agent_id,
            analysis=analysis,
            sentimentScore=sentiment_score,
            confidence=confidence,
            createdAt=datetime.now(timezone.utc),
        )
