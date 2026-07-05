@echo off
setlocal EnableDelayedExpansion

title Phoenix AI Trader - Genera Licenza

echo.
echo =======================================
echo  Phoenix AI Trader - Genera Licenza
echo =======================================
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
  echo.
  echo Prima esegui setup_windows.bat nella stessa cartella.
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
echo Genero licenza...
echo.

py ..\generate_license.py generate --private-key phoenix_private_key.pem --email "%CUSTOMER_EMAIL%" --customer-name "%CUSTOMER_NAME%" --plan pro %EXPIRES_ARG% > licenza_generata.txt
if errorlevel 1 (
  echo ERRORE: generazione licenza fallita.
  pause
  exit /b 1
)

type licenza_generata.txt

echo.
echo =======================================
echo  Licenza salvata in licenza_generata.txt
echo =======================================
echo.
echo Copia il codice che inizia con PHX1. e invialo al cliente.
echo.
pause
endlocal
