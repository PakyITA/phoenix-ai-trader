<div align="center">

<img src="docs/logo.png" width="180" alt="Logo Phoenix AI Trader">

# 🦅 Phoenix AI Trader

### Paper Trading per Home Assistant

**Simula • Monitora • Impara • Migliora**

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1+-41BDF5?style=for-the-badge)
![Demo](https://img.shields.io/badge/Demo-24h-orange?style=for-the-badge)
![Versione](https://img.shields.io/badge/version-0.3.2-blue?style=for-the-badge)
![Licenza](https://img.shields.io/badge/license-commercial-red?style=for-the-badge)

</div>

---

## 🇮🇹 Cos'è Phoenix AI Trader

**Phoenix AI Trader** è un'integrazione per **Home Assistant** pensata per simulare un portafoglio crypto in modalità **Paper Trading**.

L'obiettivo è permettere all'utente di configurare un capitale virtuale, monitorare guadagni/perdite, seguire una missione personale e ricevere dati direttamente dentro Home Assistant tramite sensori nativi e pannello dedicato.

> ⚠️ **Phoenix AI Trader non esegue trading reale.**
>
> Non si collega a Binance, Bybit, Coinbase o altri exchange e non invia ordini reali.

---

## 🧱 Separazione dal vecchio progetto Python

Da questa versione l'integrazione Home Assistant è separata dal vecchio progetto Python.

### Vecchio progetto Python

Il vecchio progetto può continuare a usare i suoi file, ad esempio:

```text
/config/phoenix-ai-trader/status.json
```

### Integrazione Home Assistant

L'integrazione Home Assistant usa invece una cartella dedicata:

```text
/config/phoenix-ai-trader-ha
```

Dentro questa cartella vengono creati file con nomi specifici:

```text
phoenix_status.json
phoenix_settings.json
phoenix_history.json
phoenix_trades.json
```

Questa separazione evita che Home Assistant legga per errore il vecchio `status.json` del progetto Python.

---

## ✨ Funzioni principali

### 🏠 Integrazione nativa Home Assistant

Phoenix crea sensori nativi utilizzabili in dashboard, automazioni e notifiche.

Esempi di sensori:

- Equity
- Liquidità
- Capitale investito
- Profitto/perdita aperta
- Profitto totale
- Win rate
- Trade aperti
- Trade chiusi
- Top crypto
- Ultimo aggiornamento
- Stato licenza
- Tempo demo residuo

---

## ⚙️ Wizard di configurazione

Dopo l'installazione, Phoenix si configura da:

```text
Impostazioni → Dispositivi e servizi → Aggiungi integrazione → Phoenix AI Trader
```

Durante il wizard puoi impostare:

- Cartella dati
- Capitale iniziale
- Capitale obiettivo
- Durata della missione
- Email
- Codice di attivazione opzionale
- Notifiche Telegram opzionali
- Soglia di alert in euro
- Soglia di alert in percentuale
- Tempo minimo tra un alert e l'altro

La cartella predefinita è:

```text
/config/phoenix-ai-trader-ha
```

---

## 📊 Dashboard integrata

Phoenix include un pannello laterale dentro Home Assistant con una dashboard dedicata.

La dashboard mostra:

- Valore portafoglio
- Equity
- Guadagno/perdita
- Stato demo/licenza
- Progressione missione
- Posizioni aperte
- Statistiche principali

<p align="center">
  <img src="docs/dashboard.png" width="95%" alt="Anteprima dashboard Phoenix AI Trader">
</p>

---

## 📱 Notifiche Telegram

Phoenix può inviare un avviso tramite un servizio `notify` di Home Assistant quando il portafoglio virtuale supera una determinata soglia di guadagno o perdita.

Esempio di servizio:

```text
notify.telegram
```

Oppure, se in Home Assistant il servizio Telegram ha un altro nome, puoi inserirlo nel wizard.

---

## ⏳ Demo 24 ore

Phoenix include una demo locale di 24 ore.

Durante la demo l'utente può provare dashboard e sensori. Alla scadenza, Phoenix può bloccare le funzioni principali fino all'inserimento di un codice di attivazione valido.

> Nota: la demo è locale/offline. Senza un backend online di licenze, un utente tecnico potrebbe comunque aggirare i controlli locali.

---

## 🔒 Sicurezza

Phoenix AI Trader è pensato esclusivamente per **Paper Trading**.

Phoenix:

✅ non gestisce denaro reale  
✅ non esegue ordini reali  
✅ non si collega ad exchange crypto  
✅ non richiede API key di trading  
✅ lavora localmente dentro Home Assistant  

---

## 📦 Installazione tramite HACS

1. Apri HACS
2. Vai su **Integrazioni**
3. Aggiungi questo repository come custom repository
4. Installa **Phoenix AI Trader**
5. Riavvia Home Assistant
6. Vai su **Impostazioni → Dispositivi e servizi**
7. Aggiungi **Phoenix AI Trader**
8. Completa il wizard

---

## 🧹 Nota per chi usava il vecchio progetto

Se sul sistema esiste già:

```text
/config/phoenix-ai-trader/status.json
```

non è un problema: da questa versione l'integrazione Home Assistant non lo usa più.

Per una nuova installazione pulita usa la cartella predefinita:

```text
/config/phoenix-ai-trader-ha
```

Se avevi già configurato Phoenix in Home Assistant con la vecchia cartella, elimina l'integrazione da **Dispositivi e servizi** e aggiungila di nuovo usando la nuova cartella.

---

## 🛣️ Funzioni previste

Possibili sviluppi futuri:

- Alert Telegram più avanzati
- Grafici interattivi
- Report PDF
- Spiegazioni AI dei trade virtuali
- Confronto strategie
- Multi-portafoglio
- Statistiche storiche
- Backend licenze online

---

## 📜 Licenza

Phoenix AI Trader è software proprietario commerciale.

Una licenza valida concede l'uso personale e non trasferibile sulla propria istanza Home Assistant. Non è consentito redistribuire, rivendere, sublicenziare, pubblicare copie modificate o rendere il software disponibile a terzi senza autorizzazione scritta.

---

<div align="center">

## 🦅 Phoenix AI Trader

**Paper Trading per Home Assistant.**

Creato con ❤️ da PakyITA.

</div>
