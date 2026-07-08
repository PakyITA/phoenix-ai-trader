from __future__ import annotations

import math
from datetime import datetime
from typing import Any

DEFAULT_SYMBOLS = [
    "BTC",
    "ETH",
    "SOL",
    "BNB",
    "XRP",
    "ADA",
    "AVAX",
    "DOGE",
    "DOT",
    "LINK",
    "MATIC",
    "LTC",
    "ATOM",
    "NEAR",
    "ARB",
    "OP",
    "UNI",
    "APT",
    "INJ",
    "RUNE",
]

SYMBOL_NAMES = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "BNB": "BNB",
    "XRP": "XRP",
    "ADA": "Cardano",
    "AVAX": "Avalanche",
    "DOGE": "Dogecoin",
    "DOT": "Polkadot",
    "LINK": "Chainlink",
    "MATIC": "Polygon",
    "LTC": "Litecoin",
    "ATOM": "Cosmos",
    "NEAR": "NEAR Protocol",
    "ARB": "Arbitrum",
    "OP": "Optimism",
    "UNI": "Uniswap",
    "APT": "Aptos",
    "INJ": "Injective",
    "RUNE": "THORChain",
}


def _quality(score: int) -> str:
    if score >= 80:
        return "Molto alta"
    if score >= 70:
        return "Alta"
    if score >= 60:
        return "Media"
    return "Bassa"


def _confidence(score: int) -> str:
    if score >= 78:
        return "Alta"
    if score >= 62:
        return "Media"
    return "Bassa"


def _risk(score: int) -> str:
    if score >= 78:
        return "Basso"
    if score >= 62:
        return "Medio"
    return "Alto"


def _stable_wave(symbol: str, minute_bucket: int) -> float:
    seed = sum((index + 1) * ord(char) for index, char in enumerate(symbol))
    return math.sin((seed + minute_bucket) / 7.0) + math.cos((seed * 2 + minute_bucket) / 11.0)


def build_crypto_scan(status: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a lightweight paper-trading market scan.

    Phoenix is currently a paper-trading simulator, so this scanner produces a
    deterministic local watchlist without placing trades or using exchange API keys.
    It gives the dashboard useful ranked setups while the real market-data backend
    is developed.
    """
    now = datetime.now()
    minute_bucket = int(now.timestamp() // 300)
    symbols = DEFAULT_SYMBOLS
    rows: list[dict[str, Any]] = []

    for index, symbol in enumerate(symbols):
        wave = _stable_wave(symbol, minute_bucket)
        base = 62 + (wave * 12) + ((len(symbol) + index) % 7)
        score = max(35, min(95, int(round(base))))
        change_24h = round(wave * 2.7, 2)
        trend = "LONG" if score >= 68 else "WAIT"

        rows.append(
            {
                "symbol": symbol,
                "name": SYMBOL_NAMES.get(symbol, symbol),
                "pair": f"{symbol}/USDT",
                "score": score,
                "confidence": _confidence(score),
                "quality": _quality(score),
                "market_risk": _risk(score),
                "signal": trend,
                "change_24h_percent": change_24h,
                "paper_trading": True,
                "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    rows.sort(key=lambda item: item["score"], reverse=True)
    top = rows[0] if rows else {}

    return {
        "online": True,
        "last_update": now.strftime("%Y-%m-%d %H:%M:%S"),
        "scanned_count": len(rows),
        "top20": rows[:20],
        "top_crypto": top.get("symbol", "N/D"),
        "top_crypto_name": top.get("name", "N/D"),
        "top_pair": top.get("pair", "N/D"),
        "top_score": top.get("score", 0),
        "top_confidence": top.get("confidence", "N/D"),
        "top_quality": top.get("quality", "N/D"),
        "market_risk": top.get("market_risk", "N/D"),
        "last_trade": "N/D",
    }
