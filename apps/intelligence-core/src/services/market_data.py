from datetime import datetime, timezone
from ..types import MarketData


def get_market_data(ticker: str) -> MarketData:
    return MarketData(
        ticker=ticker,
        price=100.0,
        volume=250000.0,
        commodityCorrelations=[{"commodity": "coal", "coefficient": 0.63}],
        timestamp=datetime.now(timezone.utc),
    )
