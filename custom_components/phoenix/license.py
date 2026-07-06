from __future__ import annotations

import base64
import json
from datetime import datetime, timedelta
from typing import Any

try:
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
except Exception:  # pragma: no cover - Home Assistant normally includes cryptography
    InvalidSignature = Exception
    Ed25519PublicKey = None

DEMO_DURATION_SECONDS = 24 * 60 * 60
LICENSE_STATUS_ACTIVE = "active"
LICENSE_STATUS_DEMO = "demo"
LICENSE_STATUS_EXPIRED = "expired"
LICENSE_STATUS_INVALID = "invalid"

# Public key used to verify licenses generated with tools/generate_license.py.
# IMPORTANT: generate your own key pair and replace this value with your public key.
# Never publish or commit the private key.
PHOENIX_PUBLIC_KEY_B64 = ""
LICENSE_PREFIX = "PHX1"


def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None

    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def normalize_license_key(value: str | None) -> str:
    return (value or "").strip().replace("\n", "").replace("\r", "").replace(" ", "")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def _public_key() -> Ed25519PublicKey | None:
    if not PHOENIX_PUBLIC_KEY_B64 or Ed25519PublicKey is None:
        return None

    try:
        return Ed25519PublicKey.from_public_bytes(base64.b64decode(PHOENIX_PUBLIC_KEY_B64))
    except Exception:
        return None


def decode_signed_license(value: str | None) -> dict[str, Any] | None:
    key = normalize_license_key(value)
    if not key:
        return None

    parts = key.split(".")
    if len(parts) != 3 or parts[0] != LICENSE_PREFIX:
        return None

    public_key = _public_key()
    if public_key is None:
        return None

    payload_b64 = parts[1]
    signature_b64 = parts[2]

    try:
        signature = _b64url_decode(signature_b64)
        public_key.verify(signature, payload_b64.encode("ascii"))
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    except (InvalidSignature, ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    except Exception:
        return None

    if payload.get("product") != "phoenix-ai-trader":
        return None

    return payload


def is_license_key_valid(value: str | None, email: str | None = None) -> bool:
    payload = decode_signed_license(value)
    if payload is None:
        return False

    license_email = str(payload.get("email", "")).strip().lower()
    configured_email = str(email or "").strip().lower()

    if license_email and configured_email and license_email != configured_email:
        return False

    expires_at = parse_dt(payload.get("expires_at"))
    if expires_at and datetime.now() > expires_at:
        return False

    return True


def _demo_expires_at(started_at: str) -> datetime:
    started = parse_dt(started_at) or datetime.now()
    return started + timedelta(seconds=DEMO_DURATION_SECONDS)


def _demo_payload(started_at: str, *, license_status: str = LICENSE_STATUS_DEMO) -> dict[str, Any]:
    expires_at = _demo_expires_at(started_at)

    return {
        "license_status": license_status,
        "demo_started_at": started_at,
        "demo_expires_at": expires_at.strftime("%Y-%m-%d %H:%M:%S"),
        "demo_duration_seconds": DEMO_DURATION_SECONDS,
        "demo_duration_hours": round(DEMO_DURATION_SECONDS / 3600, 4),
        "licensed": False,
    }


def build_license_payload(
    *,
    email: str | None,
    license_key: str | None,
    demo_started_at: str | None = None,
) -> dict[str, Any]:
    key = normalize_license_key(license_key)
    clean_email = (email or "").strip()
    started_at = demo_started_at or now_string()

    license_payload = decode_signed_license(key)
    if key and license_payload and is_license_key_valid(key, clean_email):
        return {
            "email": clean_email,
            "license_key": key,
            "license_status": LICENSE_STATUS_ACTIVE,
            "license_plan": license_payload.get("plan", "pro"),
            "license_id": license_payload.get("license_id"),
            "license_issued_at": license_payload.get("issued_at"),
            "license_expires_at": license_payload.get("expires_at"),
            "demo_started_at": started_at,
            "demo_expires_at": None,
            "demo_duration_seconds": DEMO_DURATION_SECONDS,
            "demo_duration_hours": round(DEMO_DURATION_SECONDS / 3600, 4),
            "licensed": True,
        }

    status = LICENSE_STATUS_INVALID if key else LICENSE_STATUS_DEMO
    return {
        "email": clean_email,
        "license_key": key,
        **_demo_payload(started_at, license_status=status),
    }


def evaluate_license(settings: dict[str, Any]) -> dict[str, Any]:
    license_key = normalize_license_key(settings.get("license_key"))
    email = settings.get("email")
    license_payload = decode_signed_license(license_key)

    if license_key and license_payload and is_license_key_valid(license_key, email):
        return {
            "license_status": LICENSE_STATUS_ACTIVE,
            "license_plan": license_payload.get("plan", "pro"),
            "license_id": license_payload.get("license_id"),
            "license_issued_at": license_payload.get("issued_at"),
            "license_expires_at": license_payload.get("expires_at"),
            "licensed": True,
            "demo_expired": False,
            "demo_remaining_seconds": None,
            "demo_expires_at": settings.get("demo_expires_at"),
            "demo_duration_seconds": DEMO_DURATION_SECONDS,
        }

    started_at = settings.get("demo_started_at") or settings.get("created_at") or now_string()
    expires = _demo_expires_at(started_at)
    remaining = int((expires - datetime.now()).total_seconds())
    status = LICENSE_STATUS_INVALID if license_key else LICENSE_STATUS_DEMO

    if remaining <= 0:
        return {
            "license_status": LICENSE_STATUS_INVALID if license_key else LICENSE_STATUS_EXPIRED,
            "licensed": False,
            "demo_expired": True,
            "demo_remaining_seconds": 0,
            "demo_expires_at": expires.strftime("%Y-%m-%d %H:%M:%S"),
            "demo_duration_seconds": DEMO_DURATION_SECONDS,
        }

    return {
        "license_status": status,
        "licensed": False,
        "demo_expired": False,
        "demo_remaining_seconds": remaining,
        "demo_expires_at": expires.strftime("%Y-%m-%d %H:%M:%S"),
        "demo_duration_seconds": DEMO_DURATION_SECONDS,
    }
