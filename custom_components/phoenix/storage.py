from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from .const import (
    DEFAULT_ALERT_COOLDOWN_HOURS,
    DEFAULT_ALERT_THRESHOLD_EUR,
    DEFAULT_ALERT_THRESHOLD_PERCENT,
    DEFAULT_TELEGRAM_ENABLED,
    DEFAULT_TELEGRAM_SERVICE,
    HISTORY_FILENAME,
    SETTINGS_FILENAME,
    STATUS_FILENAME,
    TRADES_FILENAME,
)
from .license import build_license_payload, evaluate_license


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def status_path(data_dir: str) -> str:
    return os.path.join(data_dir, STATUS_FILENAME)


def settings_path(data_dir: str) -> str:
    return os.path.join(data_dir, SETTINGS_FILENAME)


def history_path(data_dir: str) -> str:
    return os.path.join(data_dir, HISTORY_FILENAME)


def trades_path(data_dir: str) -> str:
    return os.path.join(data_dir, TRADES_FILENAME)


def ensure_data_files(
    data_dir: str,
    start_capital: float,
    target_capital: float,
    duration_value: int,
    duration_unit: str,
    email: str | None = None,
    license_key: str | None = None,
    telegram_enabled: bool = DEFAULT_TELEGRAM_ENABLED,
    telegram_service: str = DEFAULT_TELEGRAM_SERVICE,
    alert_threshold_eur: float = DEFAULT_ALERT_THRESHOLD_EUR,
    alert_threshold_percent: float = DEFAULT_ALERT_THRESHOLD_PERCENT,
    alert_cooldown_hours: int = DEFAULT_ALERT_COOLDOWN_HOURS,
) -> None:
    os.makedirs(data_dir, exist_ok=True)
    now = now_string()
    settings_file = settings_path(data_dir)
    status_file = status_path(data_dir)

    existing_settings = read_json(settings_file, default={})
    existing_status = read_json(status_file, default={})
    existing_license = {
        "email": existing_settings.get("email", email),
        "license_key": existing_settings.get("license_key", license_key),
        "demo_started_at": existing_settings.get("demo_started_at"),
    }
    license_payload = build_license_payload(
        email=existing_license["email"],
        license_key=existing_license["license_key"],
        demo_started_at=existing_license["demo_started_at"],
    )

    settings = {
        "paper_trading": True,
        "start_capital": start_capital,
        "target_capital": target_capital,
        "duration_value": duration_value,
        "duration_unit": duration_unit,
        "created_at": existing_settings.get("created_at", now),
        "currency": "€",
        "telegram_enabled": existing_settings.get("telegram_enabled", telegram_enabled),
        "telegram_service": existing_settings.get("telegram_service", telegram_service),
        "alert_threshold_eur": float(existing_settings.get("alert_threshold_eur", alert_threshold_eur)),
        "alert_threshold_percent": float(existing_settings.get("alert_threshold_percent", alert_threshold_percent)),
        "alert_cooldown_hours": int(existing_settings.get("alert_cooldown_hours", alert_cooldown_hours)),
        "last_alert_at": existing_settings.get("last_alert_at"),
        "last_alert_direction": existing_settings.get("last_alert_direction"),
        "last_alert_value": existing_settings.get("last_alert_value"),
        **license_payload,
    }

    default_status = {
        "online": False,
        "version": "0.3.0",
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
        "closed_profit": 0.0,
        "open_positions": 0,
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
        "mission": {
            "start_capital": start_capital,
            "target_capital": target_capital,
            "duration_value": duration_value,
            "duration_unit": duration_unit,
            "start_date": now,
        },
        "positions": [],
        "top20": [],
    }

    merged_settings = {**existing_settings, **settings}
    license_state = evaluate_license(merged_settings)
    commercial_state = {
        **license_state,
        "email": merged_settings.get("email", ""),
        "trial_mode": license_state["license_status"] == "demo",
        "commercial_mode": True,
        "locked": license_state["demo_expired"],
        "telegram_enabled": merged_settings.get("telegram_enabled", False),
        "telegram_service": merged_settings.get("telegram_service", DEFAULT_TELEGRAM_SERVICE),
        "alert_threshold_eur": merged_settings.get("alert_threshold_eur", DEFAULT_ALERT_THRESHOLD_EUR),
        "alert_threshold_percent": merged_settings.get("alert_threshold_percent", DEFAULT_ALERT_THRESHOLD_PERCENT),
        "alert_cooldown_hours": merged_settings.get("alert_cooldown_hours", DEFAULT_ALERT_COOLDOWN_HOURS),
    }

    write_json(settings_file, merged_settings)
    write_json(status_file, {**default_status, **existing_status, "version": "0.3.0", **commercial_state})
    write_json_if_missing(history_path(data_dir), [])
    write_json_if_missing(trades_path(data_dir), [])


def update_settings(data_dir: str, updates: dict[str, Any]) -> None:
    settings = read_settings(data_dir)
    write_json(settings_path(data_dir), {**settings, **updates})


def write_json_if_missing(path: str, payload: Any) -> None:
    if not os.path.exists(path):
        write_json(path, payload)


def write_json(path: str, payload: Any) -> None:
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)


def read_json(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_settings(data_dir: str) -> dict[str, Any]:
    return read_json(settings_path(data_dir), default={})


def read_status(data_dir: str) -> dict[str, Any]:
    path = status_path(data_dir)
    if not os.path.exists(path):
        return {"online": False, "error": "status.json not found"}

    status = read_json(path, default={})
    settings = read_settings(data_dir)
    license_state = evaluate_license(settings)

    return {
        **status,
        **license_state,
        "email": settings.get("email", ""),
        "trial_mode": license_state["license_status"] == "demo",
        "commercial_mode": True,
        "locked": license_state["demo_expired"],
        "telegram_enabled": settings.get("telegram_enabled", False),
        "telegram_service": settings.get("telegram_service", DEFAULT_TELEGRAM_SERVICE),
        "alert_threshold_eur": settings.get("alert_threshold_eur", DEFAULT_ALERT_THRESHOLD_EUR),
        "alert_threshold_percent": settings.get("alert_threshold_percent", DEFAULT_ALERT_THRESHOLD_PERCENT),
        "alert_cooldown_hours": settings.get("alert_cooldown_hours", DEFAULT_ALERT_COOLDOWN_HOURS),
    }
