function phoenixAuthHeaders() {
  try {
    const raw = localStorage.getItem("hassTokens");
    const token = raw ? JSON.parse(raw).access_token : null;
    return token ? { Authorization: `Bearer ${token}` } : {};
  } catch (error) {
    return {};
  }
}

function phoenixSetText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function phoenixSetValue(id, value) {
  const el = document.getElementById(id);
  if (el) el.value = value ?? "";
}

function phoenixGetValue(id) {
  const el = document.getElementById(id);
  return el ? el.value : "";
}

async function phoenixFetchStatus() {
  const response = await fetch("/local/phoenix-ai-trader-ha/status.json?ts=" + Date.now(), {
    credentials: "same-origin",
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return await response.json();
}

async function phoenixCallService(service, payload) {
  const response = await fetch(`/api/services/phoenix/${service}`, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      ...phoenixAuthHeaders(),
    },
    body: JSON.stringify(payload || {}),
  });

  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response;
}

async function phoenixResetMission() {
  const ok = confirm("Vuoi resettare la missione Phoenix? Capitale, tempo e statistiche paper trading torneranno ai valori configurati.");
  if (!ok) return;

  const button = document.getElementById("phoenixResetMissionBtn");
  if (button) button.disabled = true;

  try {
    await phoenixCallService("reset_mission", {});
    localStorage.removeItem("phoenixAiTraderMission");
    alert("Missione Phoenix resettata.");
    if (typeof load === "function") {
      await load();
    } else {
      window.location.reload();
    }
  } catch (error) {
    alert("Reset non riuscito. Riavvia Home Assistant e riprova, oppure esegui il servizio phoenix.reset_mission da Strumenti per sviluppatori.");
  } finally {
    if (button) button.disabled = false;
  }
}

async function phoenixOpenSettings() {
  const panel = document.getElementById("phoenixSettingsPanel");
  if (!panel) return;
  panel.classList.add("open");
  phoenixSetText("phoenixSettingsStatus", "Caricamento impostazioni...");

  try {
    const d = await phoenixFetchStatus();
    const mission = d.mission || {};
    phoenixSetValue("phoenixSetStartCapital", d.start_balance ?? mission.start_capital ?? 1000);
    phoenixSetValue("phoenixSetTargetCapital", d.target_capital ?? mission.target_capital ?? 10000);
    phoenixSetValue("phoenixSetDurationValue", mission.duration_value ?? 1);
    phoenixSetValue("phoenixSetDurationUnit", mission.duration_unit ?? "years");
    phoenixSetValue("phoenixSetEmail", d.email ?? "");
    phoenixSetValue("phoenixSetActivationCode", "");
    phoenixSetValue("phoenixSetTelegramEnabled", String(Boolean(d.telegram_enabled)));
    phoenixSetValue("phoenixSetTelegramService", d.telegram_service ?? "notify.telegram");
    phoenixSetValue("phoenixSetThresholdEur", d.alert_threshold_eur ?? 10);
    phoenixSetValue("phoenixSetThresholdPercent", d.alert_threshold_percent ?? 1);
    phoenixSetValue("phoenixSetCooldownHours", d.alert_cooldown_hours ?? 24);
    phoenixSetText("phoenixSettingsStatus", "Impostazioni caricate. Modifica i valori e salva.");
  } catch (error) {
    phoenixSetText("phoenixSettingsStatus", "Impossibile caricare le impostazioni Phoenix.");
  }
}

function phoenixCloseSettings() {
  const panel = document.getElementById("phoenixSettingsPanel");
  if (panel) panel.classList.remove("open");
}

function phoenixSettingsPayload() {
  return {
    start_capital: Number(phoenixGetValue("phoenixSetStartCapital") || 0),
    target_capital: Number(phoenixGetValue("phoenixSetTargetCapital") || 0),
    duration_value: Number(phoenixGetValue("phoenixSetDurationValue") || 1),
    duration_unit: phoenixGetValue("phoenixSetDurationUnit") || "years",
    email: phoenixGetValue("phoenixSetEmail").trim(),
    activation_code: phoenixGetValue("phoenixSetActivationCode").trim(),
    telegram_enabled: phoenixGetValue("phoenixSetTelegramEnabled") === "true",
    telegram_service: phoenixGetValue("phoenixSetTelegramService").trim() || "notify.telegram",
    alert_threshold_eur: Number(phoenixGetValue("phoenixSetThresholdEur") || 0),
    alert_threshold_percent: Number(phoenixGetValue("phoenixSetThresholdPercent") || 0),
    alert_cooldown_hours: Number(phoenixGetValue("phoenixSetCooldownHours") || 24),
  };
}

async function phoenixSaveSettings(resetAfterSave = false) {
  const saveButton = document.getElementById(resetAfterSave ? "phoenixSaveAndResetBtn" : "phoenixSaveSettingsBtn");
  if (saveButton) saveButton.disabled = true;
  phoenixSetText("phoenixSettingsStatus", "Salvataggio impostazioni...");

  try {
    await phoenixCallService("update_settings", phoenixSettingsPayload());
    localStorage.removeItem("phoenixAiTraderMission");

    if (resetAfterSave) {
      await phoenixCallService("reset_mission", {});
    }

    phoenixSetText("phoenixSettingsStatus", resetAfterSave ? "Impostazioni salvate e missione resettata." : "Impostazioni salvate.");
    if (typeof load === "function") await load();
  } catch (error) {
    phoenixSetText("phoenixSettingsStatus", "Errore durante il salvataggio. Controlla i log di Home Assistant.");
  } finally {
    if (saveButton) saveButton.disabled = false;
  }
}

async function phoenixTestTelegram() {
  const button = document.getElementById("phoenixTestTelegramBtn");
  if (button) button.disabled = true;
  phoenixSetText("phoenixSettingsStatus", "Invio test Telegram...");

  try {
    await phoenixCallService("test_telegram", {
      telegram_service: phoenixGetValue("phoenixSetTelegramService").trim() || "notify.telegram",
    });
    phoenixSetText("phoenixSettingsStatus", "Test Telegram inviato. Controlla Telegram.");
  } catch (error) {
    phoenixSetText("phoenixSettingsStatus", "Test Telegram non riuscito. Verifica il servizio notify e i log di Home Assistant.");
  } finally {
    if (button) button.disabled = false;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const resetButton = document.getElementById("phoenixResetMissionBtn");
  if (resetButton) resetButton.addEventListener("click", phoenixResetMission);

  const openSettingsButton = document.getElementById("phoenixOpenSettingsBtn");
  if (openSettingsButton) openSettingsButton.addEventListener("click", phoenixOpenSettings);

  const closeSettingsButton = document.getElementById("phoenixCloseSettingsBtn");
  if (closeSettingsButton) closeSettingsButton.addEventListener("click", phoenixCloseSettings);

  const testTelegramButton = document.getElementById("phoenixTestTelegramBtn");
  if (testTelegramButton) testTelegramButton.addEventListener("click", phoenixTestTelegram);

  const saveSettingsButton = document.getElementById("phoenixSaveSettingsBtn");
  if (saveSettingsButton) saveSettingsButton.addEventListener("click", () => phoenixSaveSettings(false));

  const saveAndResetButton = document.getElementById("phoenixSaveAndResetBtn");
  if (saveAndResetButton) saveAndResetButton.addEventListener("click", () => phoenixSaveSettings(true));
});
