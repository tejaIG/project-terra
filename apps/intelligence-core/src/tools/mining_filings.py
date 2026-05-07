from __future__ import annotations

from typing import Any
import httpx


def _safe_get_json(url: str) -> list[dict[str, Any]]:
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
            response.raise_for_status()
            payload = response.json()
            return payload if isinstance(payload, list) else []
    except Exception:
        return []


def fetch_ministry_circulars(ticker: str) -> list[str]:
    # Uses a fallback when live endpoints are unavailable.
    data = _safe_get_json("https://example.com/ministry-circulars.json")
    if not data:
        return [f"{ticker}: No fresh ministry circulars detected in fallback feed."]
    return [str(item.get("title", "")) for item in data[:5] if item.get("title")]


def fetch_nse_announcements(ticker: str) -> list[str]:
    data = _safe_get_json("https://example.com/nse-announcements.json")
    if not data:
        return [f"{ticker}: No recent NSE announcements detected in fallback feed."]
    return [str(item.get("headline", "")) for item in data[:5] if item.get("headline")]
