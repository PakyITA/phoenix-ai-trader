# 🔐 Flusso licenze Phoenix AI Trader

Questo documento descrive il flusso consigliato per vendere Phoenix AI Trader manualmente tramite PayPal e inviare la licenza al cliente via email.

---

## Flusso commerciale

1. Il cliente paga tramite PayPal.
2. Ricevi la notifica PayPal con email e nome del cliente.
3. Generi una licenza firmata usando lo script locale.
4. Invi la licenza al cliente via email.
5. Il cliente inserisce la licenza in Home Assistant da:

```text
Impostazioni → Dispositivi e servizi → Phoenix AI Trader → Configura
```

---

## Prima configurazione

Installa la libreria necessaria sul tuo PC:

```bash
pip install cryptography
```

Genera la coppia di chiavi:

```bash
python tools/generate_license.py init-keys
```

Verranno creati due file:

```text
phoenix_private_key.pem
phoenix_public_key.txt
```

⚠️ `phoenix_private_key.pem` deve restare solo sul tuo PC. Non caricarlo mai su GitHub.

Copia il contenuto di:

```text
phoenix_public_key.txt
```

nel file:

```text
custom_components/phoenix/license.py
```

sostituendo:

```python
PHOENIX_PUBLIC_KEY_B64 = ""
```

con:

```python
PHOENIX_PUBLIC_KEY_B64 = "LA_TUA_CHIAVE_PUBBLICA"
```

---

## Generare una licenza dopo pagamento PayPal

Esempio licenza lifetime:

```bash
python tools/generate_license.py generate --email cliente@email.it --customer-name "Mario Rossi" --plan pro
```

Esempio licenza annuale:

```bash
python tools/generate_license.py generate --email cliente@email.it --customer-name "Mario Rossi" --plan pro --expires-at 2027-12-31
```

Lo script stamperà una licenza simile a:

```text
PHX1.eyJjdXN0b21lcl9uYW1lIjoiTWFyaW8gUm9zc2kiLCJlbWFpbCI6ImNsaWVudGVAZW1haWwuaXQiLCJleHBpcmVzX2F0IjpudWxsLCJpc3N1ZWRfYXQiOiIyMDI2LTA3LTA1IDE5OjAwOjAwIiwibGljZW5zZV9pZCI6IlBIWC1BQkMxMjMiLCJwbGFuIjoicHJvIiwicHJvZHVjdCI6InBob2VuaXgtYWktdHJhZGVyIn0.FIRMA_DIGITALE
```

Questa è la licenza da inviare al cliente.

---

## Email consigliata al cliente

Oggetto:

```text
Licenza Phoenix AI Trader
```

Testo:

```text
Ciao,

grazie per aver acquistato Phoenix AI Trader.

Questa è la tua licenza personale:

INCOLLA_QUI_LA_LICENZA

Per attivarla:

1. Apri Home Assistant
2. Vai su Impostazioni → Dispositivi e servizi
3. Apri Phoenix AI Trader
4. Clicca Configura
5. Inserisci email e codice licenza
6. Salva

La licenza è personale e non trasferibile.

Grazie,
Phoenix AI Trader
```

---

## Sicurezza

- La chiave privata genera le licenze.
- La chiave pubblica verifica le licenze dentro Home Assistant.
- La chiave privata non deve mai essere pubblicata.
- Il repository può essere pubblico perché contiene solo la chiave pubblica.

---

## Nota importante

Questo sistema non richiede server ed è adatto per una prima vendita manuale.

Quando le vendite cresceranno, il passo successivo consigliato è un backend licenze online per gestire revoche, rinnovi e attivazioni per singolo dispositivo.
