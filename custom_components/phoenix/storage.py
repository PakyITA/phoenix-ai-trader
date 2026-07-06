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


PHOENIX_VERSION = "0.3.5"


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


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "N/D"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _round_money(value: float) -> float:
    return round(float(value), 2)


def normalize_accounting(status: dict[str, Any]) -> dict[str, Any]:
    """Keep Phoenix accounting internally coherent.

    The dashboard and sensors should not trust stale P/L values blindly. The source
    of truth is:
      - invested_amount: capital actually allocated to open positions
      - open_value: current value of open positions
      - balance: free liquidity
      - start_balance: initial paper-trading capital

    From those values we derive unrealized P/L, equity and total P/L. This avoids
    a common bug where commissions or stale total_profit values make Phoenix look
    permanently in loss.
    """
    data = dict(status or {})
    positions = data.get("positions") or []

    position_invested = 0.0
    position_value = 0.0
    position_pnl = 0.0
    normalized_positions: list[dict[str, Any]] = []

    if isinstance(positions, list):
        for raw_position in positions:
            if not isinstance(raw_position, dict):
                continue

            position = dict(raw_position)
            amount = _num(position.get("amount") or position.get("invested") or position.get("cost"))
            current_value = _num(
                position.get("current_value")
                or position.get("value")
                or position.get("market_value")
            )

            # If the engine only writes quantity/current price, rebuild current value.
            quantity = _num(position.get("quantity") or position.get("qty"))
            current_price = _num(position.get("current_price") or position.get("price"))
            if current_value == 0 and quantity > 0 and current_price > 0:
                current_value = quantity * current_price

            pnl = current_value - amount if amount > 0 else _num(position.get("pnl"))
            change_percent = (pnl / amount * 100) if amount > 0 else 0.0

            position["amount"] = _round_money(amount)
            position["current_value"] = _round_money(current_value)
            position["pnl"] = _round_money(pnl)
            position["change_percent"] = round(change_percent, 2)
            normalized_positions.append(position)

            position_invested += amount
            position_value += current_value
            position_pnl += pnl

    invested_amount = _num(data.get("invested_amount"))
    open_value = _num(data.get("open_value"))

    if normalized_positions:
        invested_amount = position_invested
        open_value = position_value

    balance = _num(data.get("balance"))
    start_balance = _num(
        data.get("start_balance")
        or (data.get("mission") or {}).get("start_capital")
        or data.get("initial_capital")
        or balance
    )

    unrealized_pnl = open_value - invested_amount if invested_amount > 0 else position_pnl
    equity = balance + open_value
    if equity == 0 and start_balance > 0:
        equity = start_balance + unrealized_pnl + _num(data.get("closed_profit"))

    closed_profit = _num(data.get("closed_profit"))
    total_profit = equity - start_balance if start_balance > 0 else closed_profit + unrealized_pnl
    total_profit_percent = (total_profit / start_balance * 100) if start_balance > 0 else 0.0
    unrealized_percent = (unrealized_pnl / invested_amount * 100) if invested_amount > 0 else 0.0

    previous_max_profit = _num(data.get("max_profit"), total_profit)
    previous_max_loss = _num(data.get("max_loss"), total_profit)

    data.update(
        {
            "positions": normalized_positions,
            "open_positions": len(normalized_positions),
            "start_balance": _round_money(start_balance),
            "balance": _round_money(balance),
            "invested_amount": _round_money(invested_amount),
            "open_value": _round_money(open_value),
            "unrealized_pnl": _round_money(unrealized_pnl),
            "unrealized_pnl_percent": round(unrealized_percent, 2),
            "equity": _round_money(equity),
            "total_profit": _round_money(total_profit),
            "total_profit_percent": round(total_profit_percent, 2),
            "max_profit": _round_money(max(previous_max_profit, total_profit)),
            "max_loss": _round_money(min(previous_max_loss, total_profit)),
        }
    )
    return data


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
        "closed_profit": 0.0,
        "max_profit": 0.0,
        "max_loss": 0.0,
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
    write_json(status_file, normalize_accounting({**default_status, **existing_status, "version": PHOENIX_VERSION, **commercial_state}))
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
        return {"online": False, "error": f"{STATUS_FILENAME} not found"}

    status = read_json(path, default={})
    settings = read_settings(data_dir)
    license_state = evaluate_license(settings)

    merged = {
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
    normalized = normalize_accounting(merged)

    # Persist only when derived values changed, so the web dashboard and HA sensors
    # stay aligned without constantly rewriting the file.
    keys_to_check = {
        "positions",
        "open_positions",
        "invested_amount",
        "open_value",
        "unrealized_pnl",
        "unrealized_pnl_percent",
        "equity",
        "total_profit",
        "total_profit_percent",
        "max_profit",
        "max_loss",
    }
    if any(status.get(key) != normalized.get(key) for key in keys_to_check):
        write_json(path, normalized)

    return normalized
