<div align="center">

<img src="docs/logo.png" width="180" alt="Logo Phoenix AI Trader">

# 🦅 Phoenix AI Trader

### Paper Trading con AI per Home Assistant

**Simula • Impara • Migliora**

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1+-41BDF5?style=for-the-badge)
![Demo](https://img.shields.io/badge/Demo-24h-orange?style=for-the-badge)
![Versione](https://img.shields.io/badge/version-0.3.2-blue?style=for-the-badge)
![Licenza](https://img.shields.io/badge/license-commercial-red?style=for-the-badge)

**🇬🇧 Documentazione inglese:** [README.md](README.md)

---

**Phoenix AI Trader** porta una piattaforma avanzata di **Paper Trading** direttamente dentro **Home Assistant**.

Puoi testare strategie, monitorare un portafoglio virtuale, seguire le performance e migliorare il tuo processo decisionale senza rischiare denaro reale.

> ⚠️ **Phoenix AI Trader è progettato esclusivamente per il Paper Trading.**
>
> Non si collega agli exchange crypto e non esegue ordini reali.

</div>

---

## ✨ Funzioni principali

### 🧠 Paper Trading con AI

Crea e gestisci un portafoglio crypto completamente virtuale.

Ideale per:

- imparare i concetti base del trading
- testare nuove strategie
- migliorare disciplina e metodo
- monitorare performance simulate
- creare automazioni Home Assistant basate sugli eventi del portafoglio

---

### 📊 Dashboard professionale

Phoenix include una dashboard integrata in Home Assistant con:

- 💰 valore del portafoglio
- 📈 equity
- 📉 profitto / perdita
- 🎯 avanzamento missione
- 🏆 migliori opportunità
- 📊 win rate
- 🪙 loghi delle criptovalute
- 🧠 AI score
- 🔐 stato demo / licenza

<p align="center">
  <img src="docs/dashboard.png" width="95%" alt="Anteprima dashboard Phoenix AI Trader">
</p>

---

### 🏠 Integrazione nativa Home Assistant

Phoenix crea entità native Home Assistant come:

- Equity
- Liquidità
- Capitale investito
- Valore posizioni aperte
- Profitto / perdita aperta
- Profitto totale
- Profitto percentuale
- Win rate
- Trade aperti
- Trade chiusi
- Top cryptocurrency
- Ultimo aggiornamento
- Stato licenza
- Tempo demo residuo

Queste entità possono essere usate in dashboard, automazioni, script e notifiche.

---

### ⚙️ Wizard di configurazione automatico

Dopo l'installazione, configura Phoenix da:

```text
Impostazioni → Dispositivi e servizi → Aggiungi integrazione → Phoenix AI Trader
```

Durante il wizard puoi configurare:

- cartella dati
- capitale iniziale
- capitale obiettivo
- durata della missione
- email
- codice di attivazione opzionale
- notifiche Telegram opzionali
- soglia alert guadagno / perdita in euro
- soglia alert guadagno / perdita in percentuale
- tempo minimo tra un alert e l'altro

Non è richiesta alcuna configurazione YAML manuale.

---

## 🧱 Separazione dal vecchio progetto Python

Phoenix AI Trader nasce inizialmente come progetto Python standalone.

Dalla versione **0.3.2**, l'integrazione Home Assistant utilizza una cartella dati dedicata:

```text
/config/phoenix-ai-trader-ha
```

L'integrazione crea automaticamente questi file:

```text
phoenix_status.json
phoenix_settings.json
phoenix_history.json
phoenix_trades.json
```

Questa separazione evita conflitti con vecchie installazioni Python standalone che potrebbero ancora usare:

```text
/config/phoenix-ai-trader/status.json
```

Se avevi già configurato Phoenix in Home Assistant con la vecchia cartella, elimina l'integrazione da **Dispositivi e servizi** e aggiungila nuovamente usando la nuova cartella predefinita.

---

## ⏳ Demo 24 ore

Phoenix AI Trader include una demo locale completa di 24 ore.

Durante la demo puoi provare dashboard e sensori. Alla scadenza, Phoenix può bloccare dashboard e sensori principali fino all'inserimento di un codice di attivazione valido.

> Nota: il sistema demo attuale è locale/offline. Senza un backend online di licenze, un utente tecnico potrebbe comunque aggirare i controlli locali.

---

## 🎯 Mission Mode

Imposta la tua sfida personale di investimento virtuale.

Puoi configurare:

- capitale iniziale
- capitale obiettivo
- durata

Phoenix traccia automaticamente:

- avanzamento del capitale
- avanzamento temporale
- completamento dell'obiettivo

---

## 📱 Notifiche Telegram

Phoenix può inviare avvisi tramite un servizio `notify` di Home Assistant quando il portafoglio simulato raggiunge una soglia configurata di guadagno o perdita.

Esempio di servizio:

```text
notify.telegram
```

Se il servizio Telegram nel tuo Home Assistant ha un nome diverso, puoi inserirlo nel wizard.

---

## 📦 Installazione con HACS

1. Apri HACS
2. Vai su **Integrazioni**
3. Aggiungi questo repository come custom repository
4. Installa **Phoenix AI Trader**
5. Riavvia Home Assistant
6. Vai su **Impostazioni → Dispositivi e servizi**
7. Aggiungi **Phoenix AI Trader**
8. Completa il wizard

---

## 📁 Cartella dati predefinita

```text
/config/phoenix-ai-trader-ha
```

L'integrazione genera automaticamente tutti i file necessari dentro questa cartella.

---

## 🔒 Sicurezza

Phoenix AI Trader è **100% Paper Trading**.

Phoenix:

✅ non si collega a Binance  
✅ non si collega a Bybit  
✅ non si collega a Coinbase  
✅ non esegue trade reali  
✅ non gestisce fondi reali  
✅ non richiede API key di exchange  

Tutto viene simulato localmente dentro Home Assistant.

---

## 📡 Funzioni previste

Le prossime versioni potrebbero includere:

- 📱 notifiche Telegram avanzate
- 📈 alert guadagno / perdita
- 🤖 assistente trading AI
- 📊 grafici interattivi
- 📄 report PDF
- 📈 confronto strategie
- 🧠 spiegazioni AI dei trade
- 🌍 supporto multi-portafoglio
- 📚 statistiche trading
- 📉 analisi storiche
- 🔐 backend licenze online

---

## 📜 Licenza

Phoenix AI Trader è software proprietario commerciale.

Una licenza valida concede l'utilizzo personale e non trasferibile sulla propria istanza Home Assistant.

Non è consentito redistribuire, rivendere, sublicenziare, pubblicare copie modificate o rendere il software disponibile a terzi senza autorizzazione scritta.

---

<div align="center">

## 🦅 Phoenix AI Trader

**Paper Trading con AI per Home Assistant.**

Creato con ❤️ da PakyITA.

</div>
