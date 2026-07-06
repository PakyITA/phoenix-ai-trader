#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import secrets
from datetime import datetime
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

LICENSE_PREFIX = "PHX1"
PRODUCT = "phoenix-ai-trader"


def b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def load_private_key(path: Path) -> Ed25519PrivateKey:
    return serialization.load_pem_private_key(path.read_bytes(), password=None)


def save_key_pair(private_key_path: Path, public_key_path: Path) -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )

    private_key_path.write_bytes(private_pem)
    public_key_path.write_text(base64.b64encode(public_raw).decode("ascii"), encoding="utf-8")

    print("OK - Key pair generated")
    print(f"Private key: {private_key_path}")
    print(f"Public key:  {public_key_path}")
    print("\nWARNING - Keep the private key secret. Never commit it to GitHub.")
    print("Copy the public key value into PHOENIX_PUBLIC_KEY_B64 inside custom_components/phoenix/license.py")


def generate_license(
    *,
    private_key_path: Path,
    email: str,
    plan: str,
    expires_at: str | None,
    customer_name: str | None,
) -> str:
    private_key = load_private_key(private_key_path)
    issued_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    license_id = "PHX-" + secrets.token_hex(6).upper()

    payload = {
        "product": PRODUCT,
        "license_id": license_id,
        "email": email.strip().lower(),
        "customer_name": (customer_name or "").strip(),
        "plan": plan.strip().lower(),
        "issued_at": issued_at,
        "expires_at": expires_at,
    }

    payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload_b64 = b64url_encode(payload_json)
    signature = private_key.sign(payload_b64.encode("ascii"))
    signature_b64 = b64url_encode(signature)

    return f"{LICENSE_PREFIX}.{payload_b64}.{signature_b64}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Phoenix AI Trader offline license generator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-keys", help="Generate a private/public key pair")
    init_parser.add_argument("--private-key", default="phoenix_private_key.pem")
    init_parser.add_argument("--public-key", default="phoenix_public_key.txt")

    gen_parser = subparsers.add_parser("generate", help="Generate a signed license")
    gen_parser.add_argument("--private-key", default="phoenix_private_key.pem")
    gen_parser.add_argument("--email", required=True)
    gen_parser.add_argument("--plan", default="pro")
    gen_parser.add_argument("--expires-at", default=None, help="Optional expiry date, e.g. 2027-12-31. Leave empty for lifetime.")
    gen_parser.add_argument("--customer-name", default=None)

    args = parser.parse_args()

    if args.command == "init-keys":
        save_key_pair(Path(args.private_key), Path(args.public_key))
        return

    if args.command == "generate":
        license_key = generate_license(
            private_key_path=Path(args.private_key),
            email=args.email,
            plan=args.plan,
            expires_at=args.expires_at,
            customer_name=args.customer_name,
        )
        print("\nOK - Phoenix AI Trader license generated\n")
        print(license_key)
        print("\nSend this license to the customer and ask them to paste it into Phoenix AI Trader > Configure.")


if __name__ == "__main__":
    main()
