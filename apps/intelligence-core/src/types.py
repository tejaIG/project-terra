from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class AgentId(str, Enum):
    geologist = "geologist"
    quant = "quant"
    oracle = "oracle"
    strategist = "strategist"


class CommodityCorrelation(BaseModel):
    commodity: str
    coefficient: float


class MarketData(BaseModel):
    ticker: str
    price: float
    volume: float
    commodityCorrelations: List[CommodityCorrelation] = Field(default_factory=list)
    timestamp: datetime


class AgentAnalysis(BaseModel):
    agentId: AgentId
    analysis: str
    sentimentScore: float
    confidence: float
    createdAt: datetime


class RiskParams(BaseModel):
    stopLossPct: float
    takeProfitPct: float
    maxPositionSizePct: float


class TradeAction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class TradeSignal(BaseModel):
    ticker: str
    action: TradeAction
    rationale: str
    riskParams: RiskParams


class AnalyzeResponse(BaseModel):
    runId: str
    ticker: str
    marketData: MarketData
    analyses: List[AgentAnalysis]
    finalSignal: Optional[TradeSignal] = None


class RunRequest(BaseModel):
    ticker: str


class RunResponse(BaseModel):
    runId: str


class ApproveTradeRequest(BaseModel):
    runId: str
    signal: TradeSignal
