from __future__ import annotations

from typing import Any

from .accounting import normalize_accounting
from .storage import (
    PHOENIX_VERSION,
    _license_overlay,
    history_path,
    now_string,
    read_json,
    settings_path,
    status_path,
    trades_path,
    write_json,
)


def reset_mission(data_dir: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = read_json(settings_path(data_dir), default={})
    status = read_json(status_path(data_dir), default={})
    current = {**settings, **(config or {})}
    now = now_string()

    start_capital = float(current.get("start_capital") or status.get("start_balance") or 1000.0)
    target_capital = float(current.get("target_capital") or status.get("target_capital") or start_capital)
    duration_value = int(current.get("duration_value") or 1)
    duration_unit = str(current.get("duration_unit") or "years")

    updated_settings = {
        **settings,
        "start_capital": start_capital,
        "target_capital": target_capital,
        "duration_value": duration_value,
        "duration_unit": duration_unit,
        "last_alert_at": None,
        "last_alert_direction": None,
        "last_alert_value": None,
    }
    write_json(settings_path(data_dir), updated_settings)

    reset_status = {
        **status,
        "version": PHOENIX_VERSION,
        "paper_trading": True,
        "last_update": now,
        "scanned_count": 0,
        "start_balance": start_capital,
        "balance": start_capital,
        "invested_amount": 0.0,
        "open_value": 0.0,
        "unrealized_pnl": 0.0,
        "unrealized_pnl_percent": 0.0,
        "equity": start_capital,
        "total_profit": 0.0,
        "total_profit_percent": 0.0,
        "target_capital": target_capital,
        "target_distance": max(0.0, target_capital - start_capital),
        "target_progress_percent": 0.0,
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

    normalized = normalize_accounting({**reset_status, **_license_overlay(updated_settings)})
    write_json(status_path(data_dir), normalized)
    write_json(history_path(data_dir), [])
    write_json(trades_path(data_dir), [])
    return normalized
