import asyncio
from src.council import build_council
from src.services.event_bus import EventBus
from src.services.market_data import get_market_data


def test_council_compiles():
    bus = EventBus()
    graph = build_council(bus)
    state = {
        "ticker": "NMDC",
        "market_data": get_market_data("NMDC"),
        "run_id": "run-1",
        "geologist": None,
        "quant": None,
        "oracle": None,
        "strategist": None,
        "signal": None,
    }
    result = asyncio.run(graph.ainvoke(state))
    assert result["signal"] is not None
