from uuid import uuid4
from fastapi import APIRouter, Request
from ..council import build_council
from ..services.event_bus import EventBus
from ..services.market_data import get_market_data
from ..types import AnalyzeResponse

router = APIRouter(prefix="", tags=["analysis"])


@router.post("/analyze/{ticker}", response_model=AnalyzeResponse)
async def analyze_ticker(ticker: str, request: Request) -> AnalyzeResponse:
    bus: EventBus = request.app.state.event_bus
    run_id = str(uuid4())
    market_data = get_market_data(ticker)
    council = build_council(bus)
    state = {
        "ticker": ticker,
        "market_data": market_data,
        "run_id": run_id,
        "geologist": None,
        "quant": None,
        "oracle": None,
        "signal": None,
    }
    result = await council.ainvoke(state)
    responses = [result["geologist"], result["quant"], result["oracle"]]
    return AnalyzeResponse(
        runId=run_id,
        ticker=ticker,
        marketData=market_data,
        responses=responses,
        finalSignal=result["signal"],
    )
