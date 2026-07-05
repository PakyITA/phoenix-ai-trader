from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

DEMO_DURATION_HOURS = 24
LICENSE_STATUS_ACTIVE = "active"
LICENSE_STATUS_DEMO = "demo"
LICENSE_STATUS_EXPIRED = "expired"
LICENSE_STATUS_INVALID = "invalid"

# Local/offline license keys for the first commercial version.
# This is intentionally simple: without a server, every local Python check can be bypassed.
# Replace this with online validation when Phoenix gets a license backend.
VALID_OFFLINE_LICENSE_KEYS = {
    "PHOENIX-PRO-2026",
    "PHOENIX-DEV-PRO",
}


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def normalize_license_key(value: str | None) -> str:
    return (value or "").strip().upper()


def is_license_key_valid(value: str | None) -> bool:
    return normalize_license_key(value) in VALID_OFFLINE_LICENSE_KEYS


def build_license_payload(
    *,
    email: str | None,
    license_key: str | None,
    demo_started_at: str | None = None,
) -> dict[str, Any]:
    key = normalize_license_key(license_key)
    started_at = demo_started_at or now_string()

    if key and is_license_key_valid(key):
        return {
            "email": (email or "").strip(),
            "license_key": key,
            "license_status": LICENSE_STATUS_ACTIVE,
            "demo_started_at": started_at,
            "demo_expires_at": None,
            "demo_duration_hours": DEMO_DURATION_HOURS,
            "licensed": True,
        }

    expires_at = parse_dt(started_at) or datetime.now()
    expires_at = expires_at + timedelta(hours=DEMO_DURATION_HOURS)

    return {
        "email": (email or "").strip(),
        "license_key": key,
        "license_status": LICENSE_STATUS_DEMO,
        "demo_started_at": started_at,
        "demo_expires_at": expires_at.strftime("%Y-%m-%d %H:%M:%S"),
        "demo_duration_hours": DEMO_DURATION_HOURS,
        "licensed": False,
    }


def evaluate_license(settings: dict[str, Any]) -> dict[str, Any]:
    license_key = normalize_license_key(settings.get("license_key"))

    if license_key and is_license_key_valid(license_key):
        return {
            "license_status": LICENSE_STATUS_ACTIVE,
            "licensed": True,
            "demo_expired": False,
            "demo_remaining_seconds": None,
            "demo_expires_at": settings.get("demo_expires_at"),
        }

    started_at = settings.get("demo_started_at") or settings.get("created_at") or now_string()
    started = parse_dt(started_at) or datetime.now()
    expires = started + timedelta(hours=DEMO_DURATION_HOURS)
    remaining = int((expires - datetime.now()).total_seconds())

    if remaining <= 0:
        return {
            "license_status": LICENSE_STATUS_EXPIRED,
            "licensed": False,
            "demo_expired": True,
            "demo_remaining_seconds": 0,
            "demo_expires_at": expires.strftime("%Y-%m-%d %H:%M:%S"),
        }

    return {
        "license_status": LICENSE_STATUS_DEMO,
        "licensed": False,
        "demo_expired": False,
        "demo_remaining_seconds": remaining,
        "demo_expires_at": expires.strftime("%Y-%m-%d %H:%M:%S"),
    }
