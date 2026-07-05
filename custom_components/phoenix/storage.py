from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from .const import HISTORY_FILENAME, SETTINGS_FILENAME, STATUS_FILENAME, TRADES_FILENAME
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
) -> None:
    os.makedirs(data_dir, exist_ok=True)
    now = now_string()
    settings_file = settings_path(data_dir)

    existing_settings = read_json(settings_file, default={})
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
        **license_payload,
    }

    status = {
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

    write_json(settings_file, {**existing_settings, **settings})
    write_json_if_missing(status_path(data_dir), status)
    write_json_if_missing(history_path(data_dir), [])
    write_json_if_missing(trades_path(data_dir), [])


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
    }
