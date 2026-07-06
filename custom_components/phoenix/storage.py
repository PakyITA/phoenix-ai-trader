from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from .accounting import normalize_accounting
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


PHOENIX_VERSION = "0.4.0"
PUBLIC_STATUS_DIR = "/config/www/phoenix-ai-trader-ha"


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


def _mirror_public_status(path: str, payload: Any) -> None:
    if os.path.basename(path) != STATUS_FILENAME:
        return
    try:
        os.makedirs(PUBLIC_STATUS_DIR, exist_ok=True)
        public_path = os.path.join(PUBLIC_STATUS_DIR, STATUS_FILENAME)
        with open(public_path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)
    except OSError:
        pass


def write_json(path: str, payload: Any) -> None:
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
    _mirror_public_status(path, payload)


def read_json(path: str, default: Any) -> Any:
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json_if_missing(path: str, payload: Any) -> None:
    if not os.path.exists(path):
        write_json(path, payload)


def read_settings(data_dir: str) -> dict[str, Any]:
    return read_json(settings_path(data_dir), default={})


def update_settings(data_dir: str, updates: dict[str, Any]) -> None:
    settings = read_settings(data_dir)
    write_json(settings_path(data_dir), {**settings, **updates})


def _license_overlay(settings: dict[str, Any]) -> dict[str, Any]:
    license_state = evaluate_license(settings)
    return {
        **license_state,
        "email": settings.get("email", ""),
        "trial_mode": license_state["license_status"] == "demo",
        "locked": license_state["demo_expired"],
        "telegram_enabled": settings.get("telegram_enabled", False),
        "telegram_service": settings.get("telegram_service", DEFAULT_TELEGRAM_SERVICE),
        "alert_threshold_eur": settings.get("alert_threshold_eur", DEFAULT_ALERT_THRESHOLD_EUR),
        "alert_threshold_percent": settings.get("alert_threshold_percent", DEFAULT_ALERT_THRESHOLD_PERCENT),
        "alert_cooldown_hours": settings.get("alert_cooldown_hours", DEFAULT_ALERT_COOLDOWN_HOURS),
    }


def _append_history(data_dir: str, status: dict[str, Any]) -> None:
    path = history_path(data_dir)
    history = read_json(path, default=[])
    if not isinstance(history, list):
        history = []

    snapshot = {
        "time": status.get("last_update") or now_string(),
        "equity": status.get("equity"),
        "total_profit": status.get("total_profit"),
        "total_profit_percent": status.get("total_profit_percent"),
        "target_progress_percent": status.get("target_progress_percent"),
        "open_positions": status.get("open_positions"),
    }
    if not history or history[-1] != snapshot:
        history.append(snapshot)
        write_json(path, history[-500:])


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
    existing_settings = read_json(settings_path(data_dir), default={})
    existing_status = read_json(status_path(data_dir), default={})

    license_payload = build_license_payload(
        email=existing_settings.get("email", email),
        license_key=existing_settings.get("license_key", license_key),
        demo_started_at=existing_settings.get("demo_started_at"),
    )
    settings = {
        **existing_settings,
        "paper_trading": True,
        "start_capital": start_capital,
        "target_capital": target_capital,
        "duration_value": duration_value,
        "duration_unit": duration_unit,
        "created_at": existing_settings.get("created_at", now),
        "currency": "EUR",
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

    write_json(settings_path(data_dir), settings)
    status = normalize_accounting({**default_status, **existing_status, "version": PHOENIX_VERSION, **_license_overlay(settings)})
    write_json(status_path(data_dir), status)
    write_json_if_missing(history_path(data_dir), [])
    write_json_if_missing(trades_path(data_dir), [])


def read_status(data_dir: str) -> dict[str, Any]:
    path = status_path(data_dir)
    if not os.path.exists(path):
        return {"online": False, "error": f"{STATUS_FILENAME} not found"}

    status = read_json(path, default={})
    settings = read_settings(data_dir)
    normalized = normalize_accounting({**status, "version": PHOENIX_VERSION, **_license_overlay(settings)})

    keys = {
        "version",
        "positions",
        "metrics",
        "raw_accounting",
        "accounting_model",
        "accounting_note",
        "open_positions",
        "invested_amount",
        "open_value",
        "unrealized_pnl",
        "unrealized_pnl_percent",
        "equity",
        "total_profit",
        "total_profit_percent",
        "target_capital",
        "target_distance",
        "target_progress_percent",
        "max_profit",
        "max_loss",
    }
    if any(status.get(key) != normalized.get(key) for key in keys):
        write_json(path, normalized)
        _append_history(data_dir, normalized)
    else:
        _mirror_public_status(path, normalized)

    return normalized
