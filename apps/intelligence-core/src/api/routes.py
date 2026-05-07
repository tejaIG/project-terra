import asyncio
from uuid import uuid4
from fastapi import APIRouter, Header, HTTPException, Request
from ..council import build_council
from ..services.event_bus import EventBus
from ..services.events import emit_error, emit_run_completed, emit_run_started
from ..services.market_data import get_market_data
from ..services.supabase_client import get_supabase_client
from ..services.tick_simulator import stream_ticks
from ..services.persistence import save_user_trade
from ..services import broker
from ..types import ApproveTradeRequest, RunRequest, RunResponse

router = APIRouter(prefix="", tags=["analysis"])


@router.post("/runs", response_model=RunResponse)
async def create_run(payload: RunRequest, request: Request) -> RunResponse:
    bus: EventBus = request.app.state.event_bus
    run_id = str(uuid4())
    ticker = payload.ticker

    async def run_council() -> None:
        market_data = get_market_data(ticker)
        council = build_council(bus)
        stop_event = asyncio.Event()
        tick_task = asyncio.create_task(stream_ticks(bus, run_id, market_data, stop_event))
        await emit_run_started(bus, run_id, ticker)
        try:
            state = {
                "ticker": ticker,
                "market_data": market_data,
                "run_id": run_id,
                "geologist": None,
                "quant": None,
                "oracle": None,
                "strategist": None,
                "signal": None,
            }
            result = await council.ainvoke(state)
            await emit_run_completed(bus, run_id, result["signal"])
        except Exception as exc:
            await emit_error(bus, run_id, str(exc))
            await emit_run_completed(bus, run_id, None)
        finally:
            stop_event.set()
            await tick_task

    asyncio.create_task(run_council())
    return RunResponse(runId=run_id)


@router.post("/trades")
async def approve_trade(
    payload: ApproveTradeRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, str]:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", maxsplit=1)[1]
    supabase = get_supabase_client()
    if supabase is None:
        raise HTTPException(status_code=503, detail="Supabase is not configured")
    user_response = supabase.auth.get_user(token)
    user = user_response.user
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    await save_user_trade(payload.runId, payload.signal.ticker, user.id, payload.signal)
    await broker.execute(payload.signal)
    return {"status": "approved"}
