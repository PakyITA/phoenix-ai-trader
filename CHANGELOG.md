# Changelog

All notable changes to **Phoenix AI Trader** are documented here.

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
- README and Italian README updated for version 0.4.1.

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

---

## Italiano

## [0.4.1] - 2026-07-13

### Corretto

- Risolto il problema degli alert Telegram bloccati da MarkdownV2.
- Phoenix ora fa escape automatico dei caratteri riservati Telegram MarkdownV2 prima di inviare i messaggi.
- Corretto l'errore Telegram:

```text
Can't parse entities: character '.' is reserved and must be escaped
```

### Modificato

- Gli alert Telegram automatici ora usano chiamate Home Assistant bloccanti, così gli errori sono più visibili nei log.
- I payload Telegram sono semplificati e usano direttamente il servizio notify configurato in Home Assistant.
- La versione interna Phoenix è stata allineata alla versione del manifest HACS.
- Aggiornati README inglese e README italiano alla versione 0.4.1.

### Migliorato

- Istruzioni Telegram più chiare.
- Aggiunti comandi di diagnostica log Home Assistant:

```bash
ha core logs -n 200 | grep -i phoenix
ha core logs -n 200 | grep -i telegram
```

### Note

- Phoenix resta una integrazione **solo Paper Trading**.
- Non si collega ad exchange reali.
- Non esegue ordini reali.

---

## [0.4.0] - 2026-07-09

### Aggiunto

- Pannello laterale Phoenix dentro Home Assistant.
- Vista avanzamento missione con capitale obiettivo e durata.
- Motore automatico di paper trading.
- Apertura simulata di posizioni virtuali su setup crypto con score elevato.
- Scanner crypto con classifica delle migliori opportunità.
- Alert Telegram per:
  - buy virtuali automatici
  - setup di mercato con score alto
  - soglie profit/loss
- Azione Test Telegram dalla pagina impostazioni Phoenix.
- Diagnostica Telegram nello status Phoenix:
  - `last_telegram_at`
  - `last_telegram_status`
  - `last_telegram_context`
  - `last_telegram_error`
- Persistenza privata di codice attivazione e Telegram Chat ID.
- Cancellazione sicura dei valori privati salvati usando `CLEAR`.
- Mirror pubblici dello status:
  - `/config/www/phoenix-ai-trader-ha/status.json`
  - `/config/www/phoenix-ai-trader-ha/phoenix_status.json`
- Supporto dashboard italiano/inglese.
- Demo gratuita di 24 ore.
- Supporto licenza annuale firmata.
- Disclaimer finanziario nella documentazione.

### Modificato

- Le impostazioni Phoenix si possono modificare direttamente dal pannello Phoenix.
- Le impostazioni missione vengono salvate correttamente.
- I campi privati salvati vengono mantenuti se lasciati vuoti.
- Versioni asset dashboard aggiornate per ridurre problemi di cache browser.
- Migliorato il fallback rendering dashboard sui file status.

### Corretto

- Corretto cooldown automatico stale quando non esisteva una vera posizione paper aperta.
- Corretti errori rendering dashboard causati da metadati coin mancanti.
- Corretti problemi del cambio lingua.
- Corretta generazione degli alias pubblici status.
- Corretto `last_trade` che veniva resettato durante gli scan.
