@echo off
setlocal EnableDelayedExpansion

title Phoenix AI Trader - Genera e Invia Licenza

echo.
echo =================================================
echo  Phoenix AI Trader - Genera e Invia Licenza Email
echo =================================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo ERRORE: Python Launcher ^(py^) non trovato.
  echo Installa Python e riprova.
  pause
  exit /b 1
)

if not exist phoenix_private_key.pem (
  echo ERRORE: phoenix_private_key.pem non trovato.
  echo Prima esegui setup_windows.bat nella stessa cartella.
  pause
  exit /b 1
)

if not exist email_config.json (
  echo ERRORE: email_config.json non trovato.
  echo.
  echo 1. Copia email_config.example.json
  echo 2. Rinominalo in email_config.json
  echo 3. Inserisci la password app Gmail dentro smtp_password
  echo.
  pause
  exit /b 1
)

set /p CUSTOMER_EMAIL=Email PayPal/Home Assistant cliente: 
if "%CUSTOMER_EMAIL%"=="" (
  echo ERRORE: email obbligatoria.
  pause
  exit /b 1
)

set /p CUSTOMER_NAME=Nome cliente ^(opzionale^): 

echo.
echo Tipo licenza:
echo 1 - Lifetime / senza scadenza
echo 2 - Annuale con scadenza
echo.
set /p LICENSE_TYPE=Scegli 1 o 2: 

set EXPIRES_ARG=
if "%LICENSE_TYPE%"=="2" (
  set /p EXPIRES_AT=Data scadenza ^(esempio 2027-12-31^): 
  if not "!EXPIRES_AT!"=="" set EXPIRES_ARG=--expires-at !EXPIRES_AT!
)

echo.
echo Genero e invio licenza a %CUSTOMER_EMAIL%...
echo.

py ..\send_license_email.py --config email_config.json --private-key phoenix_private_key.pem --email "%CUSTOMER_EMAIL%" --customer-name "%CUSTOMER_NAME%" --plan pro %EXPIRES_ARG% --save-license licenza_generata.txt
if errorlevel 1 (
  echo.
  echo ERRORE: generazione o invio email falliti.
  echo Controlla email_config.json, password app Gmail e connessione internet.
  pause
  exit /b 1
)

echo.
echo =================================================
echo  Operazione completata
echo =================================================
echo.
echo La licenza e' stata salvata anche in licenza_generata.txt
echo.
pause
endlocal
