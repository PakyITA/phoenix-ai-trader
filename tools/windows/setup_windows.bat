@echo off
setlocal

title Phoenix AI Trader - Setup Generatore Licenze

echo.
echo =====================================================
echo  Phoenix AI Trader - Setup Generatore Licenze Windows
echo =====================================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo ERRORE: Python Launcher ^(py^) non trovato.
  echo.
  echo Installa Python da https://www.python.org/downloads/
  echo Durante l'installazione seleziona: Add Python to PATH
  echo.
  pause
  exit /b 1
)

echo Python trovato.
echo.

echo Installo/aggiorno cryptography...
py -m pip install --upgrade pip cryptography
if errorlevel 1 (
  echo.
  echo ERRORE: installazione dipendenze fallita.
  pause
  exit /b 1
)

if exist phoenix_private_key.pem (
  echo.
  echo Chiave privata gia' presente: phoenix_private_key.pem
  echo Non genero nuove chiavi per evitare di invalidare le licenze future.
) else (
  echo.
  echo Genero la coppia di chiavi Phoenix...
  py ..\generate_license.py init-keys --private-key phoenix_private_key.pem --public-key phoenix_public_key.txt
  if errorlevel 1 (
    echo.
    echo ERRORE: generazione chiavi fallita.
    pause
    exit /b 1
  )
)

echo.
echo =====================================================
echo  Setup completato
echo =====================================================
echo.
echo File importanti creati nella cartella tools\windows:
echo.
echo - phoenix_private_key.pem  ^<-- NON pubblicare MAI
echo - phoenix_public_key.txt   ^<-- da copiare in license.py
echo.
echo Apri phoenix_public_key.txt e copia il contenuto in:
echo custom_components\phoenix\license.py
echo.
echo Dentro questa riga:
echo PHOENIX_PUBLIC_KEY_B64 = "INCOLLA_QUI_LA_CHIAVE_PUBBLICA"
echo.
pause
endlocal
