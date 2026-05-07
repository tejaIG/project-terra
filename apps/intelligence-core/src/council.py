import asyncio
from typing import Optional, TypedDict
from langgraph.graph import END, StateGraph
from .agents import GeologistAgent, OracleAgent, QuantAgent, StrategistAgent
from .services.event_bus import EventBus
from .types import AgentAnalysis, MarketData, TradeSignal


class CouncilState(TypedDict):
    ticker: str
    market_data: MarketData
    run_id: str
    geologist: Optional[AgentAnalysis]
    quant: Optional[AgentAnalysis]
    oracle: Optional[AgentAnalysis]
    strategist: Optional[AgentAnalysis]
    signal: Optional[TradeSignal]


def build_council(bus: EventBus):
    geologist = GeologistAgent(bus)
    quant = QuantAgent(bus)
    oracle = OracleAgent(bus)
    strategist = StrategistAgent(bus)
    graph = StateGraph(CouncilState)

    async def parallel_agents_node(state: CouncilState) -> CouncilState:
        geo, qnt, orc = await asyncio.gather(
            geologist.analyze(state["ticker"], state["market_data"]),
            quant.analyze(state["ticker"], state["market_data"]),
            oracle.analyze(state["ticker"], state["market_data"]),
        )
        await geologist._emit(state["run_id"], state["ticker"], geo)
        await quant._emit(state["run_id"], state["ticker"], qnt)
        await oracle._emit(state["run_id"], state["ticker"], orc)
        state["geologist"] = geo
        state["quant"] = qnt
        state["oracle"] = orc
        return state

    async def strategist_node(state: CouncilState) -> CouncilState:
        analysis = await strategist.analyze(state["ticker"], state["market_data"])
        await strategist._emit(state["run_id"], state["ticker"], analysis)
        state["strategist"] = analysis
        state["signal"] = strategist.to_signal(state["ticker"])
        return state

    graph.add_node("parallel_agents", parallel_agents_node)
    graph.add_node("strategist", strategist_node)
    graph.set_entry_point("parallel_agents")
    graph.add_edge("parallel_agents", "strategist")
    graph.add_edge("strategist", END)
    return graph.compile()
