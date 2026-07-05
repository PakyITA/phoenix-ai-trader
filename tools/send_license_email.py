#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

from generate_license import generate_license

DEFAULT_SUBJECT = "La tua licenza Phoenix AI Trader"


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Create it from tools/windows/email_config.example.json"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def build_body(*, customer_name: str | None, license_key: str) -> str:
    greeting = f"Ciao {customer_name}," if customer_name else "Ciao,"
    return f"""{greeting}

grazie per aver acquistato Phoenix AI Trader.

Questa è la tua licenza personale:

{license_key}

Per attivarla:

1. Apri Home Assistant
2. Vai su Impostazioni → Dispositivi e servizi
3. Apri Phoenix AI Trader
4. Clicca Configura
5. Inserisci la stessa email usata per PayPal
6. Incolla il codice licenza
7. Salva

Dopo il salvataggio, Phoenix verrà sbloccato.

La licenza è personale, non trasferibile e valida per una installazione Home Assistant.

Grazie,
Phoenix AI Trader
"""


def send_email(
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    sender_email: str,
    sender_name: str,
    recipient_email: str,
    subject: str,
    body: str,
) -> None:
    message = EmailMessage()
    message["From"] = f"{sender_name} <{sender_email}>" if sender_name else sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        server.login(smtp_user, smtp_password)
        server.send_message(message)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and email a Phoenix AI Trader license")
    parser.add_argument("--config", default="email_config.json", help="Local SMTP config JSON")
    parser.add_argument("--private-key", default="phoenix_private_key.pem")
    parser.add_argument("--email", required=True, help="Customer PayPal/Home Assistant email")
    parser.add_argument("--customer-name", default="", help="Customer name")
    parser.add_argument("--plan", default="pro")
    parser.add_argument("--expires-at", default=None, help="Optional expiry date, e.g. 2027-12-31")
    parser.add_argument("--save-license", default="licenza_generata.txt")
    args = parser.parse_args()

    config = load_config(Path(args.config))

    license_key = generate_license(
        private_key_path=Path(args.private_key),
        email=args.email,
        plan=args.plan,
        expires_at=args.expires_at,
        customer_name=args.customer_name,
    )

    Path(args.save_license).write_text(license_key, encoding="utf-8")

    body = build_body(customer_name=args.customer_name, license_key=license_key)

    send_email(
        smtp_host=config.get("smtp_host", "smtp.gmail.com"),
        smtp_port=int(config.get("smtp_port", 465)),
        smtp_user=config["smtp_user"],
        smtp_password=config["smtp_password"],
        sender_email=config.get("sender_email", config["smtp_user"]),
        sender_name=config.get("sender_name", "Phoenix AI Trader"),
        recipient_email=args.email,
        subject=config.get("subject", DEFAULT_SUBJECT),
        body=body,
    )

    print("✅ Licenza generata e inviata")
    print(f"Cliente: {args.email}")
    print(f"Licenza salvata in: {args.save_license}")


if __name__ == "__main__":
    main()
