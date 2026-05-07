from typing import Optional, TypedDict
from langgraph.graph import END, StateGraph
from .agents import GeologistAgent, OracleAgent, QuantAgent, StrategistAgent
from .services.event_bus import EventBus
from .types import AgentResponse, MarketData, TradeSignal


class CouncilState(TypedDict):
    ticker: str
    market_data: MarketData
    run_id: str
    geologist: Optional[AgentResponse]
    quant: Optional[AgentResponse]
    oracle: Optional[AgentResponse]
    signal: Optional[TradeSignal]


def build_council(bus: EventBus):
    strategist = StrategistAgent(bus)
    graph = StateGraph(CouncilState)
    graph.add_node("geologist", GeologistAgent(bus).run_node)
    graph.add_node("quant", QuantAgent(bus).run_node)
    graph.add_node("oracle", OracleAgent(bus).run_node)

    async def strategist_node(state: CouncilState) -> CouncilState:
        response = await strategist.analyze(state["ticker"], state["market_data"])
        await strategist._emit(state["run_id"], response)
        state["signal"] = strategist.to_signal(state["ticker"])
        return state

    graph.add_node("strategist", strategist_node)
    graph.set_entry_point("geologist")
    graph.add_edge("geologist", "quant")
    graph.add_edge("quant", "oracle")
    graph.add_edge("oracle", "strategist")
    graph.add_edge("strategist", END)
    return graph.compile()
