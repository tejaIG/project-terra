from __future__ import annotations


def fetch_et_headlines(ticker: str) -> list[str]:
    return [
        f"{ticker} sees stable demand from infrastructure spending",
        f"Analysts track commodity-linked volatility for {ticker}",
    ]


def fetch_moneycontrol_headlines(ticker: str) -> list[str]:
    return [
        f"{ticker} management reiterates cautious guidance",
        f"Broker desks flag margin watch for {ticker}",
    ]
