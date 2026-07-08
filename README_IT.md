# 🦅 Phoenix AI Trader

### Paper Trading intelligente per Home Assistant

**Simula • Impara • Migliora**

---

## Cos'è Phoenix AI Trader

Phoenix AI Trader è un'integrazione per Home Assistant progettata per simulare investimenti in criptovalute attraverso il **Paper Trading**.

Tutte le operazioni sono completamente virtuali e vengono eseguite in locale, senza collegamenti ad exchange o conti reali.

L'obiettivo è aiutare l'utente a studiare strategie di investimento, monitorare il proprio patrimonio virtuale e migliorare le proprie decisioni finanziarie in un ambiente sicuro.

> ⚠️ **Phoenix AI Trader è pensato esclusivamente per il Paper Trading.**
>
> Non si collega agli exchange, non esegue ordini reali e non gestisce denaro reale.

---

# ✨ Caratteristiche principali

## 🧠 Paper Trading

Phoenix permette di creare e monitorare un portafoglio virtuale senza utilizzare denaro reale.

È ideale per:

- imparare le basi del trading;
- testare nuove strategie;
- allenare la disciplina;
- monitorare risultati e performance;
- simulare scenari senza rischi reali.

---

## 📊 Dashboard professionale

L'integrazione crea una dashboard dedicata direttamente dentro Home Assistant.

La dashboard mostra:

- 💰 patrimonio totale;
- 📈 equity;
- 📉 guadagni e perdite;
- 🎯 avanzamento dell'obiettivo;
- 🏆 migliori opportunità;
- 📊 win rate;
- 🪙 criptovalute monitorate;
- 🧠 valutazioni AI;
- 🔐 stato demo/licenza.

---

## ⏳ Demo gratuita di 24 ore

Phoenix AI Trader include una demo completa di 24 ore.

Durante la demo l'utente può provare tutte le funzionalità principali.

Al termine della prova, la dashboard principale e i sensori vengono bloccati fino all'inserimento di un codice di attivazione valido.

> Nota: nella versione attuale il controllo demo/licenza è locale. Senza un backend online, un utente tecnico molto esperto potrebbe aggirare alcune verifiche locali.

---

## ⚙️ Configurazione guidata

Phoenix dispone di un wizard di configurazione.

Durante l'installazione è possibile configurare:

- cartella dati;
- capitale iniziale;
- obiettivo finale;
- durata della simulazione;
- email;
- codice di attivazione;
- notifiche Telegram;
- soglie di guadagno/perdita.

Non è richiesta configurazione YAML manuale.

---

## 📱 Notifiche Telegram

Phoenix può inviare notifiche automatiche tramite Home Assistant quando il portafoglio virtuale supera determinate soglie.

L'utente può configurare:

- servizio Telegram, ad esempio `notify.telegram`;
- soglia minima in euro;
- soglia minima percentuale;
- intervallo minimo tra due notifiche.

Esempio di notifica:

```text
📈 Phoenix AI Trader

Stai guadagnando +25.00 €
Rendimento: +2.50%
Equity attuale: 1025.00 €
Liquidità: 500.00 €
Investito: 525.00 €
```

---

## 🎯 Missione capitale

Phoenix permette di impostare un obiettivo personale.

Esempio:

- capitale iniziale: **1.000 €**;
- obiettivo: **10.000 €**;
- durata: **24 mesi**.

La dashboard mostra automaticamente:

- progressione del capitale;
- progressione temporale;
- andamento rispetto al piano teorico;
- scostamento positivo o negativo.

---

## 🏠 Integrazione nativa con Home Assistant

Phoenix crea sensori nativi utilizzabili nelle dashboard e nelle automazioni.

Tra i sensori disponibili:

- Equity;
- Liquidità;
- Capitale investito;
- Valore posizioni;
- Profitto/perdita aperto;
- Profitto totale;
- Profitto percentuale;
- Win Rate;
- Posizioni aperte;
- Trade chiusi;
- Migliore criptovaluta;
- Ultimo aggiornamento;
- Stato licenza;
- Tempo residuo demo.

---

## 🔒 Privacy e sicurezza

Phoenix AI Trader lavora in locale dentro Home Assistant.

L'integrazione:

✅ non si collega a Binance;

✅ non si collega a Bybit;

✅ non si collega a Coinbase;

✅ non esegue ordini reali;

✅ non gestisce fondi reali;

✅ non richiede accesso ai conti dell'utente.

Tutti i dati restano nella propria installazione Home Assistant.

---

## 📁 Cartella dati

La cartella dati predefinita è:

```text
/config/phoenix-ai-trader
```

Phoenix genera automaticamente questi file:

```text
status.json
settings.json
history.json
trades.json
```

---

## 🚀 Installazione

La modalità di distribuzione dipende dalla versione rilasciata.

Per installazione manuale:

1. Copiare la cartella `custom_components/phoenix` dentro la cartella `custom_components` di Home Assistant.
2. Riavviare Home Assistant.
3. Aprire **Impostazioni → Dispositivi e servizi**.
4. Cliccare **Aggiungi integrazione**.
5. Cercare **Phoenix AI Trader**.
6. Completare il wizard.

---

## 📡 Funzionalità previste

Funzionalità future previste o in valutazione:

- 📈 grafici interattivi;
- 📊 storico del patrimonio virtuale;
- 📄 report PDF;
- 🤖 assistente AI;
- 📱 notifiche avanzate;
- 📉 analisi statistiche;
- 🎯 gestione multi-portafoglio;
- 📚 confronto tra strategie;
- 🔐 sistema licenze online.

---

# 📜 Licenza

Phoenix AI Trader è un software commerciale proprietario.

L'acquisto di una licenza concede il diritto personale e non trasferibile di utilizzare il software sulla propria installazione Home Assistant.

Non è consentito ridistribuire, rivendere, sublicenziare, pubblicare copie modificate o rendere disponibile il software a terzi senza autorizzazione scritta dell'autore.

---

# ⚠️ Disclaimer

Phoenix AI Trader è destinato esclusivamente al **Paper Trading** e alla simulazione.

Non fornisce consulenza finanziaria, non gestisce investimenti reali e non esegue operazioni sui mercati.

L'autore non è responsabile per eventuali decisioni finanziarie prese sulla base delle simulazioni offerte dal software.

---

<div align="center">

## 🦅 Phoenix AI Trader

**Paper Trading intelligente per Home Assistant.**

Creato con ❤️ da PakyITA.

</div>
