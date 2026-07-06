from __future__ import annotations

from typing import Any

ACCOUNTING_MODEL = "raw-inputs-derived-metrics-v1"


def num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "N/D"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def money(value: float) -> float:
    return round(float(value), 2)


def percent(value: float, base: float) -> float:
    if base <= 0:
        return 0.0
    return round((value / base) * 100, 2)


def normalize_position(raw_position: dict[str, Any]) -> tuple[dict[str, Any], float, float, float]:
    position = dict(raw_position)
    quantity = num(position.get("quantity") or position.get("qty"))
    buy_price = num(position.get("buy_price") or position.get("entry_price") or position.get("avg_price"))
    current_price = num(position.get("current_price") or position.get("price") or position.get("last_price"))

    invested = num(position.get("amount") or position.get("invested") or position.get("cost"))
    if invested == 0 and quantity > 0 and buy_price > 0:
        invested = quantity * buy_price

    current_value = num(position.get("current_value") or position.get("value") or position.get("market_value"))
    if current_value == 0 and quantity > 0 and current_price > 0:
        current_value = quantity * current_price

    pnl = current_value - invested if invested > 0 else num(position.get("pnl"))
    position["amount"] = money(invested)
    position["current_value"] = money(current_value)
    position["pnl"] = money(pnl)
    position["change_percent"] = percent(pnl, invested)
    return position, invested, current_value, pnl


def normalize_accounting(status: dict[str, Any]) -> dict[str, Any]:
    data = dict(status or {})
    raw_positions = data.get("positions") or []
    normalized_positions: list[dict[str, Any]] = []
    invested_amount = 0.0
    open_value = 0.0
    unrealized_pnl = 0.0

    if isinstance(raw_positions, list):
        for raw_position in raw_positions:
            if not isinstance(raw_position, dict):
                continue
            position, invested, current_value, pnl = normalize_position(raw_position)
            normalized_positions.append(position)
            invested_amount += invested
            open_value += current_value
            unrealized_pnl += pnl

    if not normalized_positions:
        invested_amount = num(data.get("invested_amount"))
        open_value = num(data.get("open_value"))
        unrealized_pnl = open_value - invested_amount if invested_amount > 0 else num(data.get("unrealized_pnl"))

    mission = data.get("mission") if isinstance(data.get("mission"), dict) else {}
    balance = num(data.get("balance"))
    start_balance = num(data.get("start_balance") or mission.get("start_capital") or data.get("initial_capital") or balance)
    target_capital = num(mission.get("target_capital") or data.get("target_capital"))
    closed_profit = num(data.get("closed_profit"))

    equity = balance + open_value
    if equity == 0 and start_balance > 0:
        equity = start_balance + closed_profit + unrealized_pnl

    total_profit = equity - start_balance if start_balance > 0 else closed_profit + unrealized_pnl
    target_distance = target_capital - equity if target_capital > 0 else 0.0
    target_progress = 0.0
    if target_capital > start_balance:
        target_progress = max(0.0, min(100.0, percent(equity - start_balance, target_capital - start_balance)))

    previous_max_profit = num(data.get("max_profit"), total_profit)
    previous_max_loss = num(data.get("max_loss"), total_profit)

    metrics = {
        "start_balance": money(start_balance),
        "balance": money(balance),
        "invested_amount": money(invested_amount),
        "open_value": money(open_value),
        "unrealized_pnl": money(unrealized_pnl),
        "unrealized_pnl_percent": percent(unrealized_pnl, invested_amount),
        "equity": money(equity),
        "total_profit": money(total_profit),
        "total_profit_percent": percent(total_profit, start_balance),
        "target_capital": money(target_capital),
        "target_distance": money(target_distance),
        "target_progress_percent": round(target_progress, 2),
        "max_profit": money(max(previous_max_profit, total_profit)),
        "max_loss": money(min(previous_max_loss, total_profit)),
        "open_positions": len(normalized_positions),
    }

    data.update(metrics)
    data["positions"] = normalized_positions
    data["metrics"] = metrics
    data["raw_accounting"] = {
        "balance": metrics["balance"],
        "start_balance": metrics["start_balance"],
        "target_capital": metrics["target_capital"],
        "closed_profit": money(closed_profit),
        "positions_count": len(normalized_positions),
    }
    data["accounting_model"] = ACCOUNTING_MODEL
    data["accounting_note"] = "P/L calcolato da liquidità, posizioni aperte e capitale iniziale."
    return data
