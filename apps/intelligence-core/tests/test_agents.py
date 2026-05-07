import asyncio
from src.agents.geologist import GeologistAgent
from src.services.event_bus import EventBus
from src.services.market_data import get_market_data


def test_geologist_agent_response_shape():
    agent = GeologistAgent(EventBus())
    response = asyncio.run(agent.analyze("COALINDIA", get_market_data("COALINDIA")))
    assert response.agentId.value == "geologist"
    assert -1 <= response.sentimentScore <= 1
