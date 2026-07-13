<div align="center">

<img src="docs/logo.png" width="180" alt="Logo Phoenix AI Trader">

# 🦅 Phoenix AI Trader

### Paper Trading con AI per Home Assistant

**Simula il tuo portafoglio crypto. Monitora guadagni e perdite. Impara senza rischiare denaro reale.**

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1+-41BDF5?style=for-the-badge)
![Demo](https://img.shields.io/badge/Demo-24h-orange?style=for-the-badge)
![Licenza annuale](https://img.shields.io/badge/Licenza-Annuale-red?style=for-the-badge)
![Offerta Lancio](https://img.shields.io/badge/Offerta%20Lancio-9.99%E2%82%AC-orange?style=for-the-badge)
![Versione](https://img.shields.io/badge/version-0.4.1-blue?style=for-the-badge)
![Licenza](https://img.shields.io/badge/license-commercial-red?style=for-the-badge)

[![Aggiungi a Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PakyITA&repository=phoenix-ai-trader&category=integration)

**🇬🇧 Documentazione inglese:** [README.md](README.md)  
**📜 Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

**Phoenix AI Trader** porta un'esperienza premium di **Paper Trading** direttamente dentro **Home Assistant**.

Puoi creare un portafoglio crypto virtuale, monitorare guadagni e perdite, ricevere alert Telegram e seguire una missione personale sul capitale — senza collegarti a un exchange e senza rischiare denaro reale.

> ⚠️ **Phoenix AI Trader è progettato esclusivamente per il Paper Trading.**
>
> Non si collega a Binance, Bybit, Coinbase o altri exchange e non esegue ordini reali.

</div>

---

## ✅ Versione corrente

```text
0.4.1
```

### Novità principali della 0.4.1

- Corretto il problema Telegram con MarkdownV2.
- Gli alert Telegram ora fanno escape automatico dei caratteri riservati MarkdownV2.
- I messaggi Telegram del paper trading automatico funzionano con i servizi notify di Home Assistant.
- Versione interna Phoenix allineata alla versione del manifest HACS.
- Migliorate le istruzioni di diagnostica Telegram.

Changelog completo: [CHANGELOG.md](CHANGELOG.md)

---

## 🚀 Come funziona Phoenix

1. Installa Phoenix da HACS.
2. Completa il wizard di configurazione.
3. Usa la demo gratuita completa per 24 ore.
4. Dopo la demo, Phoenix richiede una licenza personale annuale.
5. Acquista la licenza tramite PayPal.
6. Ricevi la licenza firmata via email.
7. Incolla la licenza in **Phoenix AI Trader → Configura** oppure nella pagina impostazioni interna di Phoenix.

---

## 🔑 Demo gratuita e licenza annuale

Phoenix AI Trader include una **demo gratuita di 24 ore**.

Alla scadenza della demo, dashboard principale e sensori del portafoglio vengono bloccati fino all'inserimento di una licenza valida.

Le licenze Phoenix sono **annuali**. Una licenza valida sblocca Phoenix per **12 mesi dalla data di emissione**. Al termine del periodo annuale, la licenza deve essere rinnovata per continuare a usare le funzioni premium.

### 💥 Offerta lancio

Per i primi **15 giorni**, la licenza personale annuale Phoenix AI Trader è disponibile a:

```text
9,99 € invece di 19,99 €
```

Al termine dell'offerta lancio, il prezzo standard della licenza annuale sarà **19,99 €**.

Le licenze sono:

- annuali e valide per 12 mesi dalla data di emissione
- legate all'email PayPal dell'acquirente
- personali e non trasferibili
- valide per una installazione Home Assistant
- verificate localmente tramite licenza offline firmata

---

## ✨ Cosa rende Phoenix diverso

| | |
|---|---|
| 🧠 **AI Paper Trading** | Simula un portafoglio crypto e testa idee senza rischiare denaro reale |
| 🤖 **Posizioni virtuali automatiche** | Phoenix può aprire posizioni simulate in base ai setup con score elevato |
| 📊 **Dashboard Home Assistant** | Monitora equity, liquidità, posizioni aperte, profit/loss e missione |
| 📱 **Alert Telegram** | Ricevi avvisi per buy virtuali, setup interessanti e soglie profit/loss |
| 🎯 **Mission Mode** | Imposta capitale iniziale, capitale obiettivo e durata della missione |
| 🏠 **Entità native** | Usa sensori e binary sensor in dashboard, script e automazioni |
| 🔐 **Demo 24h + licenza annuale** | Prova Phoenix, poi sbloccalo con una licenza personale annuale firmata |
| 🧩 **Zero YAML** | Configurazione completa dal wizard Home Assistant |

---

## 📊 Anteprima dashboard

Phoenix include un pannello laterale dedicato dentro Home Assistant con:

- 💰 valore portafoglio
- 📈 equity
- 📉 profitto / perdita
- 🎯 avanzamento missione
- 🏆 migliori opportunità
- 📊 win rate
- 🪙 loghi delle criptovalute
- 🧠 AI score
- 🔐 stato demo / licenza
- 📱 diagnostica Telegram

<p align="center">
  <img src="docs/dashboard.png" width="95%" alt="Anteprima dashboard Phoenix AI Trader">
</p>

---

## 🏠 Entità Home Assistant

Phoenix crea entità native Home Assistant come:

### Sensori

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

### Binary sensor

- Licenza attiva
- Demo attiva
- Phoenix bloccato
- Telegram attivo

Queste entità possono essere usate in dashboard, automazioni, script e notifiche.

---

## ⚙️ Wizard di configurazione

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
- servizio notify Telegram di Home Assistant, per esempio `notify.telegram`
- Telegram Chat ID / target opzionale
- soglia alert guadagno / perdita in euro
- soglia alert guadagno / perdita in percentuale
- tempo minimo tra un alert e l'altro

Non è richiesta configurazione YAML manuale per Phoenix.

> 📱 **Requisito Telegram:** Phoenix non crea e non configura automaticamente il bot Telegram. Per ricevere gli alert Telegram devi prima configurare un servizio `notify` Telegram funzionante in Home Assistant.

---

## 🧾 Modifica licenza o impostazioni

Phoenix supporta il pulsante **Configura** di Home Assistant e una pagina impostazioni interna.

Vai su:

```text
Impostazioni → Dispositivi e servizi → Phoenix AI Trader → Configura
```

oppure apri:

```text
Phoenix AI Trader → Impostazioni Phoenix
```

Da qui puoi modificare:

- email licenza
- codice attivazione
- notifiche Telegram
- servizio notify Telegram
- Telegram Chat ID / target
- soglie alert
- impostazioni missione

I campi privati come licenza e Telegram Chat ID vengono mantenuti se lasciati vuoti. Per cancellare intenzionalmente un valore privato salvato, inserisci:

```text
CLEAR
```

---

## 📱 Notifiche Telegram — configurazione completa

Phoenix può inviare avvisi tramite un servizio `notify` di Home Assistant per:

- apertura automatica di posizioni virtuali
- setup di mercato con score elevato
- soglie simulate di guadagno/perdita
- controlli di stato/avvio Phoenix

Phoenix **non crea il bot Telegram** e **non configura automaticamente l'integrazione Telegram di Home Assistant**. Telegram deve già funzionare in Home Assistant prima che Phoenix possa usarlo.

### 1. Configura prima Telegram in Home Assistant

Prima di abilitare Telegram in Phoenix, assicurati che Home Assistant abbia già un servizio Telegram funzionante.

Esempi tipici:

```text
notify.telegram
notify.telegram_bot
notify.pasquale
notify.telegram_pasquale
```

Il nome preciso dipende dalla tua configurazione Home Assistant.

### 2. Testa manualmente il servizio notify

In Home Assistant apri:

```text
Strumenti per sviluppatori → Azioni
```

Esegui un test diretto, ad esempio:

```yaml
action: notify.telegram_pasquale
data:
  message: "Test Telegram da Home Assistant"
```

Se questo test non funziona, bisogna sistemare Telegram in Home Assistant prima di controllare Phoenix.

### 3. Inserisci i dati in Phoenix

Apri:

```text
Phoenix AI Trader → Impostazioni Phoenix
```

Compila:

```text
Telegram attivo: Sì
Servizio Telegram: notify.telegram_pasquale
Telegram Chat ID opzionale: vuoto oppure il tuo chat_id
```

Se il tuo servizio `notify.telegram` ha già un destinatario fisso configurato, puoi lasciare vuoto il campo Chat ID.

Se hai salvato un Chat ID errato, inserisci:

```text
CLEAR
```

e salva le impostazioni.

### 4. Salva e testa

Clicca:

```text
Salva impostazioni
```

Poi clicca:

```text
Test Telegram
```

Phoenix invierà questo messaggio:

```text
Test Telegram Passato
```

### 5. Compatibilità MarkdownV2

Dalla versione **0.4.1**, Phoenix fa escape automatico dei caratteri riservati Telegram MarkdownV2 prima di inviare gli alert. Questo evita errori come:

```text
Can't parse entities: character '.' is reserved and must be escaped
```

### 6. Se il test Telegram non funziona

Controlla questi punti:

1. Verifica che il bot Telegram funzioni già fuori da Phoenix.
2. Vai in **Strumenti per sviluppatori → Azioni** e prova manualmente il servizio `notify.telegram`.
3. Controlla che il nome del servizio inserito in Phoenix sia identico a quello di Home Assistant.
4. Se il servizio richiede un destinatario, inserisci il Telegram Chat ID in Phoenix.
5. Se è salvato un Chat ID errato, scrivi `CLEAR`, salva e riprova.
6. Controlla i log di Home Assistant cercando errori relativi a `phoenix`, `telegram` o `notify`.
7. Dopo l'aggiornamento di Phoenix, riavvia Home Assistant.

Comandi utili dal terminale di Home Assistant:

```bash
ha core logs -n 200 | grep -i phoenix
ha core logs -n 200 | grep -i telegram
```

---

## 📦 Installazione con HACS

### Metodo 1 — Aggiungi a Home Assistant

Clicca il badge **Aggiungi a Home Assistant** in alto in questo README.

### Metodo 2 — Repository custom manuale

1. Apri HACS
2. Vai su **Integrazioni**
3. Aggiungi questo repository come custom repository
4. Seleziona categoria **Integration**
5. Installa **Phoenix AI Trader**
6. Riavvia Home Assistant
7. Vai su **Impostazioni → Dispositivi e servizi**
8. Aggiungi **Phoenix AI Trader**
9. Completa il wizard

### Aggiornamento

Se HACS non rileva subito un nuovo commit:

1. Apri **HACS → Integrazioni → Phoenix AI Trader**.
2. Usa **Scarica di nuovo / Redownload**.
3. Riavvia Home Assistant.
4. Controlla il file di stato pubblico:

```text
/local/phoenix-ai-trader-ha/status.json
```

Il campo `version` deve corrispondere alla versione corrente.

---

## 📁 Cartella dati predefinita

```text
/config/phoenix-ai-trader-ha
```

L'integrazione genera automaticamente tutti i file necessari dentro questa cartella.

Gli status pubblici vengono anche copiati in:

```text
/config/www/phoenix-ai-trader-ha/status.json
/config/www/phoenix-ai-trader-ha/phoenix_status.json
```

---

## 🔒 Sicurezza

Phoenix AI Trader è **100% Paper Trading**.

Phoenix:

✅ Non si collega a Binance  
✅ Non si collega a Bybit  
✅ Non si collega a Coinbase  
✅ Non esegue trade reali  
✅ Non gestisce fondi reali  
✅ Non richiede API key di exchange  

Tutto è simulato localmente dentro Home Assistant.

---

## ⚠️ Disclaimer finanziario e responsabilità dell'utente

Phoenix AI Trader è uno strumento di **simulazione, studio e Paper Trading**. Non è un consulente finanziario, non fornisce raccomandazioni di investimento e non garantisce alcun risultato economico.

Tutte le informazioni, gli score, gli alert Telegram, le simulazioni e i dati mostrati da Phoenix hanno solo finalità educative e informative.

L'autore non è responsabile per:

- perdite finanziarie reali
- decisioni di investimento dell'utente
- uso improprio del software
- interpretazione errata dei dati
- danni diretti o indiretti derivanti dall'uso di Phoenix

L'utente è il solo responsabile delle proprie decisioni finanziarie. Qualsiasi operazione reale sui mercati deve essere svolta con consapevolezza, responsabilità e, quando opportuno, con il supporto di un professionista qualificato.

Phoenix AI Trader **non esegue trade reali**, **non gestisce fondi reali** e **non deve essere usato come sostituto di una consulenza finanziaria professionale**.

---

## 💬 Supporto

| | |
|---|---|
| 🐛 **Bug** | Apri una GitHub Issue |
| 💡 **Idee** | Usa GitHub Discussions o contatta lo sviluppatore |
| 🔑 **Licenza** | Licenza annuale · Offerta lancio: **9,99 € per 15 giorni**, poi **19,99 €/anno** · pagamento PayPal → licenza firmata via email |
| 📱 **Telegram** | Richiede un servizio Telegram `notify` già configurato in Home Assistant |
| 🇬🇧 **Supporto inglese** | Documentazione inglese disponibile in [README.md](README.md) |

---

## 📡 Funzioni previste

Le prossime versioni potranno includere:

- 📈 integrazione dati reali di mercato
- 📊 grafici interattivi
- 📄 report PDF
- 📈 confronto strategie
- 🧠 spiegazioni AI dei trade
- 🌍 multi-portafoglio
- 📚 statistiche di trading
- 📉 analisi storiche
- 🔐 backend licenze online

---

## 📜 Licenza

Phoenix AI Trader è software commerciale proprietario.

Una licenza annuale valida concede un uso personale e non trasferibile sulla propria istanza Home Assistant per 12 mesi dalla data di emissione.

Redistribuzione, rivendita, sublicenza, pubblicazione di copie modificate o messa a disposizione del software a terzi non sono consentite senza autorizzazione scritta.

---

<div align="center">

## 🦅 Phoenix AI Trader

**Paper Trading con AI per Home Assistant.**

Creato con ❤️ da PakyITA.

</div>
