DOMAIN = "phoenix"

CONF_DATA_DIR = "data_dir"
CONF_START_CAPITAL = "start_capital"
CONF_TARGET_CAPITAL = "target_capital"
CONF_DURATION_VALUE = "duration_value"
CONF_DURATION_UNIT = "duration_unit"
CONF_EMAIL = "email"
CONF_LICENSE_KEY = "activation_code"
CONF_TELEGRAM_ENABLED = "telegram_enabled"
CONF_TELEGRAM_SERVICE = "telegram_service"
CONF_ALERT_THRESHOLD_EUR = "alert_threshold_eur"
CONF_ALERT_THRESHOLD_PERCENT = "alert_threshold_percent"
CONF_ALERT_COOLDOWN_HOURS = "alert_cooldown_hours"

# Cartella dedicata SOLO all'integrazione Home Assistant.
# Il vecchio progetto Python può continuare a usare /config/phoenix-ai-trader/status.json
# senza interferire con i sensori e il wizard dell'integrazione.
DEFAULT_DATA_DIR = "/config/phoenix-ai-trader-ha"
DEFAULT_START_CAPITAL = 100.0
DEFAULT_TARGET_CAPITAL = 1000.0
DEFAULT_DURATION_VALUE = 7
DEFAULT_DURATION_UNIT = "days"
DEFAULT_EMAIL = ""
DEFAULT_ACTIVATION_CODE = ""
DEFAULT_TELEGRAM_ENABLED = False
DEFAULT_TELEGRAM_SERVICE = "notify.telegram"
DEFAULT_ALERT_THRESHOLD_EUR = 10.0
DEFAULT_ALERT_THRESHOLD_PERCENT = 1.0
DEFAULT_ALERT_COOLDOWN_HOURS = 24

STATUS_FILENAME = "phoenix_status.json"
SETTINGS_FILENAME = "phoenix_settings.json"
HISTORY_FILENAME = "phoenix_history.json"
TRADES_FILENAME = "phoenix_trades.json"

PLATFORMS = ["sensor"]