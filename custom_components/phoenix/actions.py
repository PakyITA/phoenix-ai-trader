from __future__ import annotations

from typing import Any

from .accounting import normalize_accounting
from .license import build_license_payload
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

CLEAR_VALUES = {"clear", "cancella", "delete", "reset", "none", "null", "-"}


def _float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def _private_string(payload: dict[str, Any], settings: dict[str, Any], key: str, stored_key: str | None = None) -> str:
    stored = stored_key or key
    if key not in payload:
        return str(settings.get(stored, "") or "").strip()
    value = str(payload.get(key) or "").strip()
    if value.lower() in CLEAR_VALUES:
        return ""
    if value == "":
        return str(settings.get(stored, "") or "").strip()
    return value


def update_phoenix_settings(data_dir: str, payload: dict[str, Any]) -> dict[str, Any]:
    settings = read_json(settings_path(data_dir), default={})
    status = read_json(status_path(data_dir), default={})
    now = now_string()

    start_capital = _float(payload.get("start_capital"), _float(settings.get("start_capital"), 100.0))
    target_capital = _float(payload.get("target_capital"), _float(settings.get("target_capital"), 1000.0))
    duration_value = _int(payload.get("duration_value"), _int(settings.get("duration_value"), 7))
    duration_unit = str(payload.get("duration_unit") or settings.get("duration_unit") or "days")
    email = str(payload.get("email") if payload.get("email") is not None else settings.get("email", "")).strip()
    activation_code = _private_string(payload, settings, "activation_code", "license_key")
    telegram_chat_id = _private_string(payload, settings, "telegram_chat_id")

    mission = status.get("mission") if isinstance(status.get("mission"), dict) else {}
    mission_changed = (
        _float(settings.get("start_capital"), start_capital) != start_capital
        or _float(settings.get("target_capital"), target_capital) != target_capital
        or _int(settings.get("duration_value"), duration_value) != duration_value
        or str(settings.get("duration_unit") or duration_unit) != duration_unit
    )

    license_payload = build_license_payload(
        email=email,
        license_key=activation_code,
        demo_started_at=settings.get("demo_started_at"),
    )

    updated_settings = {
        **settings,
        "paper_trading": True,
        "start_capital": start_capital,
        "target_capital": target_capital,
        "duration_value": duration_value,
        "duration_unit": duration_unit,
        "email": email,
        "license_key": activation_code,
        "telegram_enabled": bool(payload.get("telegram_enabled", settings.get("telegram_enabled", False))),
        "telegram_service": str(payload.get("telegram_service") or settings.get("telegram_service") or "notify.telegram").strip(),
        "telegram_chat_id": telegram_chat_id,
        "alert_threshold_eur": _float(payload.get("alert_threshold_eur"), _float(settings.get("alert_threshold_eur"), 10.0)),
        "alert_threshold_percent": _float(payload.get("alert_threshold_percent"), _float(settings.get("alert_threshold_percent"), 1.0)),
        "alert_cooldown_hours": _int(payload.get("alert_cooldown_hours"), _int(settings.get("alert_cooldown_hours"), 24)),
        **license_payload,
    }
    write_json(settings_path(data_dir), updated_settings)

    if mission_changed:
        base_status = {
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
        write_json(history_path(data_dir), [])
        write_json(trades_path(data_dir), [])
    else:
        base_status = {
            **status,
            "version": PHOENIX_VERSION,
            "last_update": now,
            "start_balance": start_capital,
            "target_capital": target_capital,
            "mission": {
                **mission,
                "start_capital": start_capital,
                "target_capital": target_capital,
                "duration_value": duration_value,
                "duration_unit": duration_unit,
            },
        }

    updated_status = normalize_accounting({**base_status, **_license_overlay(data_dir, updated_settings)})
    write_json(status_path(data_dir), updated_status)
    return updated_status


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

    normalized = normalize_accounting({**reset_status, **_license_overlay(data_dir, updated_settings)})
    write_json(status_path(data_dir), normalized)
    write_json(history_path(data_dir), [])
    write_json(trades_path(data_dir), [])
    return normalized
