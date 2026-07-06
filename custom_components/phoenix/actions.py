from __future__ import annotations

from typing import Any

from .accounting import normalize_accounting
from .storage import PHOENIX_VERSION, _license_overlay, now_string, read_json, settings_path, status_path, write_json


def reset_mission(data_dir: str) -> dict[str, Any]:
    settings = read_json(settings_path(data_dir), default={})
    status = read_json(status_path(data_dir), default={})
    now = now_string()

    start_capital = float(settings.get("start_capital") or status.get("start_balance") or 1000.0)
    target_capital = float(settings.get("target_capital") or status.get("target_capital") or start_capital)
    duration_value = int(settings.get("duration_value") or 1)
    duration_unit = str(settings.get("duration_unit") or "years")

    reset_status = {
        **status,
        "version": PHOENIX_VERSION,
        "paper_trading": True,
        "last_update": now,
        "scanned_count": 0,
        "start_balance": start_capital,
        "balance": start_capital,
        "closed_profit": 0.0,
        "max_profit": 0.0,
        "max_loss": 0.0,
        "closed_trades": 0,
        "wins": 0,
        "losses": 0,
        "win_rate": 0.0,
        "top_crypto": "N/D",
        "top_score": 0,
        "top_confidence": "N/D",
        "top_quality": "N/D",
        "market_risk": "N/D",
        "last_trade": "N/D",
        "best_trade": "N/D",
        "worst_trade": "N/D",
        "positions": [],
        "top20": [],
        "mission": {
            "start_capital": start_capital,
            "target_capital": target_capital,
            "duration_value": duration_value,
            "duration_unit": duration_unit,
            "start_date": now,
        },
    }

    normalized = normalize_accounting({**reset_status, **_license_overlay(settings)})
    write_json(status_path(data_dir), normalized)
    return normalized
