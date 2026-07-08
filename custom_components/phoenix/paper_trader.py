from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

AUTO_TRADE_MIN_SCORE = 80
AUTO_TRADE_ALLOCATION_PERCENT = 25.0
MAX_OPEN_POSITIONS = 3
AUTO_TRADE_COOLDOWN_MINUTES = 15


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "N/D"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _position_symbols(status: dict[str, Any]) -> set[str]:
    symbols: set[str] = set()
    positions = status.get("positions") if isinstance(status.get("positions"), list) else []
    for position in positions:
        if not isinstance(position, dict):
            continue
        symbol = str(position.get("symbol") or "").strip().upper()
        if symbol:
            symbols.add(symbol)
    return symbols


def maybe_open_paper_position(status: dict[str, Any], settings: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Open a virtual paper-trading position from the best market setup.

    The function never connects to an exchange and never places real orders.
    It only updates Phoenix local JSON status with a simulated position.
    """
    data = dict(status or {})
    settings = settings or {}

    if data.get("locked") or data.get("demo_expired"):
        return data, None

    if settings.get("auto_paper_trading_enabled", True) is False:
        return data, None

    cooldown_minutes = int(settings.get("auto_trade_cooldown_minutes", AUTO_TRADE_COOLDOWN_MINUTES) or AUTO_TRADE_COOLDOWN_MINUTES)
    last_trade_at = _parse_dt(data.get("last_auto_trade_at") or settings.get("last_auto_trade_at"))
    if last_trade_at and datetime.now() - last_trade_at < timedelta(minutes=cooldown_minutes):
        return data, None

    positions = data.get("positions") if isinstance(data.get("positions"), list) else []
    if len(positions) >= int(settings.get("max_open_positions", MAX_OPEN_POSITIONS) or MAX_OPEN_POSITIONS):
        return data, None

    top20 = data.get("top20") if isinstance(data.get("top20"), list) else []
    if not top20:
        return data, None

    open_symbols = _position_symbols(data)
    candidate = None
    for setup in top20:
        if not isinstance(setup, dict):
            continue
        symbol = str(setup.get("symbol") or "").strip().upper()
        score = int(_num(setup.get("score"), 0))
        if not symbol or symbol in open_symbols or score < AUTO_TRADE_MIN_SCORE:
            continue
        candidate = setup
        break

    if candidate is None:
        return data, None

    balance = _num(data.get("balance"), _num(data.get("start_balance"), 0.0))
    if balance <= 0:
        return data, None

    allocation_percent = _num(settings.get("auto_trade_allocation_percent"), AUTO_TRADE_ALLOCATION_PERCENT)
    allocation_percent = max(1.0, min(100.0, allocation_percent))
    amount = round(balance * allocation_percent / 100.0, 2)
    if amount <= 0:
        return data, None

    symbol = str(candidate.get("symbol") or "N/D").strip().upper()
    pair = str(candidate.get("pair") or f"{symbol}/USDT")
    score = int(_num(candidate.get("score"), 0))
    change_24h = _num(candidate.get("change_24h_percent"), 0.0)

    # Local paper price: until a real market-data backend is added, use a stable
    # simulated entry/current value so the accounting is coherent and transparent.
    entry_price = round(max(0.01, 1.0 + abs(change_24h) / 100.0 + score / 1000.0), 4)
    current_price = entry_price
    quantity = round(amount / entry_price, 8)

    position = {
        "symbol": symbol,
        "pair": pair,
        "name": candidate.get("name", symbol),
        "quantity": quantity,
        "entry_price": entry_price,
        "buy_price": entry_price,
        "current_price": current_price,
        "amount": amount,
        "current_value": amount,
        "score": score,
        "confidence": candidate.get("confidence", "N/D"),
        "quality": candidate.get("quality", "N/D"),
        "market_risk": candidate.get("market_risk", "N/D"),
        "opened_at": _now(),
        "paper_trading": True,
        "auto_opened": True,
        "note": "Posizione virtuale aperta automaticamente da Phoenix in Paper Trading. Nessun ordine reale eseguito.",
    }

    data["positions"] = [*positions, position]
    data["balance"] = round(balance - amount, 2)
    data["last_trade"] = f"AUTO PAPER BUY {pair} {amount:.2f} EUR"
    data["last_auto_trade_at"] = position["opened_at"]
    data["last_auto_trade_symbol"] = symbol
    data["last_auto_trade_amount"] = amount
    data["paper_trader_status"] = "active"
    data["paper_trader_note"] = "Phoenix investe automaticamente solo in Paper Trading, senza ordini reali."
    data["auto_trade_allocation_percent"] = allocation_percent
    data["auto_trade_min_score"] = AUTO_TRADE_MIN_SCORE
    data["auto_trade_cooldown_minutes"] = cooldown_minutes

    event = {
        "time": position["opened_at"],
        "type": "AUTO_PAPER_BUY",
        "symbol": symbol,
        "pair": pair,
        "amount": amount,
        "score": score,
        "paper_trading": True,
        "message": f"Phoenix ha aperto una posizione virtuale su {pair} investendo {amount:.2f} EUR.",
    }
    return data, event
