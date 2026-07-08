from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Any

TRIAL_GUARD_VERSION = 1
DEMO_DURATION_SECONDS = 24 * 60 * 60
PRIMARY_GUARD_DIR = "/config/.storage"
PRIMARY_GUARD_FILE = "phoenix_ai_trader_trial.json"
LOCAL_GUARD_FILE = ".phoenix_trial_guard.json"
PUBLIC_GUARD_FILE = "/config/www/phoenix-ai-trader-ha/.phoenix_trial_guard.json"


def now_dt() -> datetime:
    return datetime.now()


def dt_string(value: datetime | None = None) -> str:
    return (value or now_dt()).strftime("%Y-%m-%d %H:%M:%S")


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def _read_json(path: str) -> dict[str, Any]:
    try:
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _write_json(path: str, payload: dict[str, Any]) -> None:
    try:
        folder = os.path.dirname(path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2, ensure_ascii=False)
    except Exception:
        # Trial guard must never break Home Assistant startup.
        pass


def _guard_paths(data_dir: str) -> list[str]:
    digest = hashlib.sha256(str(data_dir).encode("utf-8")).hexdigest()[:16]
    return [
        os.path.join(PRIMARY_GUARD_DIR, f"{digest}_{PRIMARY_GUARD_FILE}"),
        os.path.join(data_dir, LOCAL_GUARD_FILE),
        PUBLIC_GUARD_FILE,
    ]


def _collect_markers(data_dir: str, settings: dict[str, Any]) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    if settings:
        markers.append({"source": "settings", **settings})
    for path in _guard_paths(data_dir):
        marker = _read_json(path)
        if marker:
            marker["source"] = path
            markers.append(marker)
    return markers


def _earliest_datetime(markers: list[dict[str, Any]], keys: tuple[str, ...]) -> datetime | None:
    values: list[datetime] = []
    for marker in markers:
        for key in keys:
            parsed = parse_dt(marker.get(key))
            if parsed:
                values.append(parsed)
    return min(values) if values else None


def _latest_datetime(markers: list[dict[str, Any]], keys: tuple[str, ...]) -> datetime | None:
    values: list[datetime] = []
    for marker in markers:
        for key in keys:
            parsed = parse_dt(marker.get(key))
            if parsed:
                values.append(parsed)
    return max(values) if values else None


def ensure_trial_guard(data_dir: str, settings: dict[str, Any]) -> dict[str, Any]:
    """Create and update local trial markers.

    This hardens the 24h trial against casual reset attempts such as deleting only
    phoenix_settings.json or editing demo_started_at. It is still local protection:
    a determined user with file/code access can bypass any offline Python check.
    """
    now = now_dt()
    markers = _collect_markers(data_dir, settings)

    earliest_start = _earliest_datetime(
        markers,
        ("trial_first_seen_at", "demo_started_at", "created_at"),
    ) or now
    latest_seen = _latest_datetime(markers, ("trial_last_seen_at", "last_seen_at"))

    clock_rollback = bool(latest_seen and now + timedelta(minutes=10) < latest_seen)
    expired_by_marker = any(bool(marker.get("trial_expired")) for marker in markers)
    expires_at = earliest_start + timedelta(seconds=DEMO_DURATION_SECONDS)
    expired_by_time = now >= expires_at
    force_expired = expired_by_marker or expired_by_time or clock_rollback

    reason = None
    if clock_rollback:
        reason = "clock_rollback_detected"
    elif expired_by_marker:
        reason = "previous_trial_expired"
    elif expired_by_time:
        reason = "trial_time_elapsed"

    guard = {
        "trial_guard_version": TRIAL_GUARD_VERSION,
        "trial_first_seen_at": dt_string(earliest_start),
        "trial_last_seen_at": dt_string(now),
        "trial_expires_at": dt_string(expires_at),
        "trial_expired": force_expired,
        "trial_lock_reason": reason,
        "demo_started_at": dt_string(earliest_start),
        "demo_expires_at": dt_string(expires_at),
        "demo_duration_seconds": DEMO_DURATION_SECONDS,
        "demo_force_expired": force_expired,
    }

    for path in _guard_paths(data_dir):
        _write_json(path, guard)

    return guard
