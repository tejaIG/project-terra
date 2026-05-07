from datetime import datetime, timezone
from ..types import MarketData
from .supabase_client import get_supabase_client
from ..tools import compute_correlation


def get_market_data(ticker: str) -> MarketData:
    price = 100.0
    volume = 250000.0
    supabase = get_supabase_client()
    if supabase is not None:
        result = (
            supabase.table("price_history")
            .select("close_price, volume")
            .order("ts", desc=True)
            .limit(1)
            .execute()
        )
        rows = result.data or []
        if rows:
            price = float(rows[0]["close_price"])
            volume = float(rows[0]["volume"])
    return MarketData(
        ticker=ticker,
        price=price,
        volume=volume,
        commodityCorrelations=[{"commodity": "coal", "coefficient": compute_correlation(ticker, "coal")}],
        timestamp=datetime.now(timezone.utc),
    )
