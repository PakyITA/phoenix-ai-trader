# Changelog italiano

Tutte le modifiche importanti di **Phoenix AI Trader** sono documentate qui.

🇬🇧 Changelog inglese: [CHANGELOG.md](CHANGELOG.md)

---

## [0.4.1] - 2026-07-13

### Corretto

- Risolto il problema degli alert Telegram bloccati dal parsing Telegram MarkdownV2.
- Phoenix ora fa automaticamente escape dei caratteri riservati MarkdownV2 prima di inviare gli alert.
- Corretto l'errore Telegram:

```text
Can't parse entities: character '.' is reserved and must be escaped
```

### Modificato

- Gli alert Telegram automatici ora usano chiamate Home Assistant bloccanti, così gli errori sono più facili da vedere nei log.
- I payload Telegram sono stati semplificati e usano direttamente il servizio `notify` configurato in Home Assistant.
- La versione interna Phoenix è stata allineata alla versione del manifest HACS.
- Le scritture dello status pubblico forzano la versione corrente di Phoenix, evitando valori vecchi come `0.4.0` in `status.json`.
- Gli esempi nella documentazione ora usano nomi generici come `notify.telegram_user` e `notify.user`.
- I file README sono stati standardizzati: `README.md` per inglese e `README.it.md` per italiano.

### Aggiunto

- Changelog italiano dedicato: `CHANGELOG.it.md`.
- Istruzioni più chiare per aggiornamento tramite HACS, redownload e riavvio Home Assistant.

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
