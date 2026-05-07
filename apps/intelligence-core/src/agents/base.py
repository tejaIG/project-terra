from abc import ABC, abstractmethod
from datetime import datetime, timezone
from ..types import AgentId, AgentResponse, MarketData
from ..services.event_bus import EventBus


class BaseAgent(ABC):
    def __init__(self, bus: EventBus, agent_id: AgentId) -> None:
        self.bus = bus
        self.agent_id = agent_id

    @abstractmethod
    async def analyze(self, ticker: str, market_data: MarketData) -> AgentResponse:
        raise NotImplementedError

    async def _emit(self, run_id: str, response: AgentResponse) -> None:
        await self.bus.publish(run_id, response.model_dump_json())

    async def run_node(self, state: dict) -> dict:
        response = await self.analyze(state["ticker"], state["market_data"])
        await self._emit(state["run_id"], response)
        state[self.agent_id.value] = response
        return state

    def _build_response(self, analysis: str, sentiment_score: float, confidence: float) -> AgentResponse:
        return AgentResponse(
            agentId=self.agent_id,
            analysis=analysis,
            sentimentScore=sentiment_score,
            confidence=confidence,
            createdAt=datetime.now(timezone.utc),
        )
