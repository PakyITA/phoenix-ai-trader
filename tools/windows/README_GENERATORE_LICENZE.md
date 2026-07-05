# 🔐 Generatore licenze Phoenix AI Trader per Windows

Questa cartella contiene gli script per generare licenze Phoenix AI Trader dal tuo PC Windows.

---

## 1. Requisito

Installa Python da:

```text
https://www.python.org/downloads/
```

Durante l'installazione seleziona:

```text
Add Python to PATH
```

---

## 2. Primo avvio

Fai doppio click su:

```text
setup_windows.bat
```

Questo script:

- controlla Python
- installa `cryptography`
- genera la chiave privata
- genera la chiave pubblica

Verranno creati:

```text
phoenix_private_key.pem
phoenix_public_key.txt
```

⚠️ `phoenix_private_key.pem` deve restare solo sul tuo PC. Non caricarlo mai su GitHub e non inviarlo a nessuno.

---

## 3. Copia la chiave pubblica in Phoenix

Apri:

```text
phoenix_public_key.txt
```

Copia tutto il contenuto e incollalo nel file:

```text
custom_components/phoenix/license.py
```

nella riga:

```python
PHOENIX_PUBLIC_KEY_B64 = ""
```

Esempio:

```python
PHOENIX_PUBLIC_KEY_B64 = "CHIAVE_PUBBLICA_COPIATA_DAL_FILE"
```

---

## 4. Generare una licenza cliente

Dopo che il cliente ha pagato con PayPal, fai doppio click su:

```text
genera_licenza_windows.bat
```

Lo script ti chiede:

- email PayPal/Home Assistant del cliente
- nome cliente opzionale
- tipo licenza: lifetime o annuale

Alla fine crea il file:

```text
licenza_generata.txt
```

Dentro trovi il codice licenza che inizia con:

```text
PHX1.
```

Copia quel codice e invialo al cliente.

---

## 5. Email da inviare al cliente

Oggetto:

```text
La tua licenza Phoenix AI Trader
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
5. Inserisci la stessa email usata per PayPal
6. Incolla il codice licenza
7. Salva

Dopo il salvataggio, Phoenix verrà sbloccato.

La licenza è personale, non trasferibile e valida per una installazione Home Assistant.

Grazie,
Phoenix AI Trader
```

---

## 6. Importante

Se perdi `phoenix_private_key.pem`, non potrai più generare licenze compatibili con la chiave pubblica già inserita nell'integrazione.

Fai una copia di backup sicura della chiave privata, ad esempio su una chiavetta USB conservata offline.
