from datetime import datetime, timezone
from pydantic import BaseModel
from ..types import AgentAnalysis, MarketData, TradeSignal
from .event_bus import EventBus


class AgentThoughtEvent(BaseModel):
    kind: str = "agent_thought"
    runId: str
    payload: AgentAnalysis


class PriceTickEvent(BaseModel):
    kind: str = "price_tick"
    runId: str
    payload: MarketData


class RunStartedPayload(BaseModel):
    ticker: str
    startedAt: datetime


class RunStartedEvent(BaseModel):
    kind: str = "run_started"
    runId: str
    payload: RunStartedPayload


class RunCompletedPayload(BaseModel):
    completedAt: datetime
    finalSignal: TradeSignal | None = None


class RunCompletedEvent(BaseModel):
    kind: str = "run_completed"
    runId: str
    payload: RunCompletedPayload


class ErrorPayload(BaseModel):
    message: str


class ErrorEvent(BaseModel):
    kind: str = "error"
    runId: str
    payload: ErrorPayload


async def emit_agent_thought(bus: EventBus, run_id: str, analysis: AgentAnalysis) -> None:
    await bus.publish(run_id, AgentThoughtEvent(runId=run_id, payload=analysis).model_dump_json())


async def emit_price_tick(bus: EventBus, run_id: str, market_data: MarketData) -> None:
    await bus.publish(run_id, PriceTickEvent(runId=run_id, payload=market_data).model_dump_json())


async def emit_run_started(bus: EventBus, run_id: str, ticker: str) -> None:
    payload = RunStartedPayload(ticker=ticker, startedAt=datetime.now(timezone.utc))
    await bus.publish(run_id, RunStartedEvent(runId=run_id, payload=payload).model_dump_json())


async def emit_run_completed(bus: EventBus, run_id: str, final_signal: TradeSignal | None = None) -> None:
    payload = RunCompletedPayload(completedAt=datetime.now(timezone.utc), finalSignal=final_signal)
    await bus.publish(run_id, RunCompletedEvent(runId=run_id, payload=payload).model_dump_json())
    await bus.publish(run_id, None)


async def emit_error(bus: EventBus, run_id: str, message: str) -> None:
    await bus.publish(run_id, ErrorEvent(runId=run_id, payload=ErrorPayload(message=message)).model_dump_json())
