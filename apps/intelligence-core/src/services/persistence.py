from typing import Any
from ..services.supabase_client import get_supabase_client
from ..types import AgentAnalysis, TradeSignal


def _get_equity_id(supabase: Any, ticker: str) -> str | None:
    response = (
        supabase.table("equities")
        .select("id")
        .eq("ticker", ticker)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    return rows[0]["id"] if rows else None


async def save_agent_analysis(run_id: str, ticker: str, analysis: AgentAnalysis) -> None:
    supabase = get_supabase_client()
    if supabase is None:
        return
    equity_id = _get_equity_id(supabase, ticker)
    if equity_id is None:
        return
    supabase.table("agent_analyses").insert(
        {
            "run_id": run_id,
            "equity_id": equity_id,
            "agent_id": analysis.agentId.value,
            "analysis": analysis.analysis,
            "sentiment_score": analysis.sentimentScore,
            "confidence": analysis.confidence,
            "created_at": analysis.createdAt.isoformat(),
        }
    ).execute()


async def save_user_trade(run_id: str, ticker: str, user_id: str, signal: TradeSignal) -> None:
    supabase = get_supabase_client()
    if supabase is None:
        return
    equity_id = _get_equity_id(supabase, ticker)
    if equity_id is None:
        return
    supabase.table("user_trades").insert(
        {
            "run_id": run_id,
            "equity_id": equity_id,
            "user_id": user_id,
            "action": signal.action.value,
            "rationale": signal.rationale,
            "risk_params": signal.riskParams.model_dump(),
            "approved": True,
        }
    ).execute()
