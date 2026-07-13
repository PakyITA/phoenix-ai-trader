# Changelog

All notable changes to **Phoenix AI Trader** are documented here.

🇮🇹 Italian changelog: [CHANGELOG.it.md](CHANGELOG.it.md)

---

## [0.4.1] - 2026-07-13

### Fixed

- Fixed Telegram delivery failures caused by Telegram MarkdownV2 parsing errors.
- Escaped Telegram MarkdownV2 reserved characters automatically before sending Phoenix alerts.
- Fixed messages failing with errors such as:

```text
Can't parse entities: character '.' is reserved and must be escaped
```

### Changed

- Telegram automatic alerts now use blocking Home Assistant service calls so errors are easier to detect in logs.
- Telegram alert payloads are simplified to use the configured Home Assistant notify service directly.
- Internal Phoenix version is aligned with the HACS manifest version.
- Public status JSON writes now force the current Phoenix version to avoid stale `version` values.
- Documentation examples now use generic notify service names such as `notify.telegram_user` and `notify.user`.
- Documentation files were standardized to `README.md` and `README.it.md`.

### Added

- Dedicated Italian changelog: `CHANGELOG.it.md`.
- Clearer update instructions for HACS redownload and Home Assistant restart.

### Improved

- Added clearer Telegram setup instructions.
- Added troubleshooting commands for Home Assistant logs:

```bash
ha core logs -n 200 | grep -i phoenix
ha core logs -n 200 | grep -i telegram
```

### Notes

- Phoenix remains a **Paper Trading only** integration.
- No real exchange connection is used.
- No real orders are executed.

---

## [0.4.0] - 2026-07-09

### Added

- Phoenix dashboard sidebar panel for Home Assistant.
- Mission progress view with capital target and time goal.
- Automatic paper trading engine.
- Simulated virtual buy events for high-score crypto setups.
- Crypto scanner with ranked top opportunities.
- Telegram alerts for:
  - automatic paper buy events
  - high-score market setups
  - profit/loss thresholds
- Telegram test action from the Phoenix settings panel.
- Telegram delivery diagnostics in Phoenix status:
  - `last_telegram_at`
  - `last_telegram_status`
  - `last_telegram_context`
  - `last_telegram_error`
- Private persistence for activation code and Telegram Chat ID.
- Safe clearing of saved private values using `CLEAR`.
- Public status mirrors:
  - `/config/www/phoenix-ai-trader-ha/status.json`
  - `/config/www/phoenix-ai-trader-ha/phoenix_status.json`
- Italian and English dashboard language support.
- 24-hour trial mode.
- Signed annual license support.
- Financial disclaimer in documentation.

### Changed

- Phoenix settings can be edited from inside the Phoenix panel.
- Mission settings persist correctly after save.
- Saved private fields are preserved when left empty.
- Dashboard asset versions bumped to reduce browser cache issues.
- Improved dashboard rendering fallback for status files.

### Fixed

- Fixed stale automatic trade cooldown when no real paper position existed.
- Fixed dashboard render errors caused by missing coin metadata.
- Fixed language switch rendering issues.
- Fixed public status alias generation.
- Fixed `last_trade` being reset during scans.
