from __future__ import annotations

from random import Random


def fetch_lme_spot(commodity: str) -> float:
    seeded = Random(hash(commodity) % 10000)
    return round(100.0 + seeded.random() * 50, 2)


def compute_correlation(ticker: str, commodity: str) -> float:
    seeded = Random(hash(f"{ticker}:{commodity}") % 10000)
    value = (seeded.random() * 2) - 1
    return round(value, 2)
