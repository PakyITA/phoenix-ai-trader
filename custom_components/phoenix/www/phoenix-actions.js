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

function phoenixSetPlaceholder(id, value) {
  const el = document.getElementById(id);
  if (el) el.placeholder = value ?? "";
}

function phoenixGetValue(id) {
  const el = document.getElementById(id);
  return el ? el.value : "";
}

async function phoenixFetchStatus() {
  const urls = [
    "/local/phoenix-ai-trader-ha/status.json",
    "/local/phoenix-ai-trader-ha/phoenix_status.json",
  ];
  for (const url of urls) {
    try {
      const response = await fetch(url + "?ts=" + Date.now(), { credentials: "same-origin" });
      if (response.ok) return await response.json();
    } catch (error) {}
  }
  throw new Error("Phoenix status not available");
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
  panel.scrollIntoView({ behavior: "smooth", block: "start" });
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
    phoenixSetPlaceholder("phoenixSetActivationCode", d.license_key_saved ? "Licenza già salvata — lascia vuoto per mantenerla" : "lascia vuoto per demo");
    phoenixSetValue("phoenixSetTelegramEnabled", String(Boolean(d.telegram_enabled)));
    phoenixSetValue("phoenixSetTelegramService", d.telegram_service ?? "notify.telegram");
    phoenixSetValue("phoenixSetTelegramChatId", "");
    phoenixSetPlaceholder("phoenixSetTelegramChatId", d.telegram_chat_id_saved ? "Chat ID già salvato — lascia vuoto per mantenerlo" : "es. 123456789 o -1001234567890");
    phoenixSetValue("phoenixSetThresholdEur", d.alert_threshold_eur ?? 10);
    phoenixSetValue("phoenixSetThresholdPercent", d.alert_threshold_percent ?? 1);
    phoenixSetValue("phoenixSetCooldownHours", d.alert_cooldown_hours ?? 24);
    phoenixSetText("phoenixSettingsStatus", "Impostazioni caricate. I campi privati già salvati possono restare vuoti.");
  } catch (error) {
    phoenixSetText("phoenixSettingsStatus", "Impossibile caricare le impostazioni Phoenix.");
  }
}

function phoenixCloseSettings() {
  const panel = document.getElementById("phoenixSettingsPanel");
  if (panel) panel.classList.remove("open");
}

function phoenixSettingsPayload() {
  const activationCode = phoenixGetValue("phoenixSetActivationCode").trim();
  const telegramChatId = phoenixGetValue("phoenixSetTelegramChatId").trim();
  const payload = {
    start_capital: Number(phoenixGetValue("phoenixSetStartCapital") || 0),
    target_capital: Number(phoenixGetValue("phoenixSetTargetCapital") || 0),
    duration_value: Number(phoenixGetValue("phoenixSetDurationValue") || 1),
    duration_unit: phoenixGetValue("phoenixSetDurationUnit") || "years",
    email: phoenixGetValue("phoenixSetEmail").trim(),
    telegram_enabled: phoenixGetValue("phoenixSetTelegramEnabled") === "true",
    telegram_service: phoenixGetValue("phoenixSetTelegramService").trim() || "notify.telegram",
    alert_threshold_eur: Number(phoenixGetValue("phoenixSetThresholdEur") || 0),
    alert_threshold_percent: Number(phoenixGetValue("phoenixSetThresholdPercent") || 0),
    alert_cooldown_hours: Number(phoenixGetValue("phoenixSetCooldownHours") || 24),
  };

  if (activationCode) payload.activation_code = activationCode;
  if (telegramChatId) payload.telegram_chat_id = telegramChatId;
  return payload;
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

  const payload = {
    telegram_service: phoenixGetValue("phoenixSetTelegramService").trim() || "notify.telegram",
  };
  const telegramChatId = phoenixGetValue("phoenixSetTelegramChatId").trim();
  if (telegramChatId) payload.telegram_chat_id = telegramChatId;

  try {
    await phoenixCallService("test_telegram", payload);
    phoenixSetText("phoenixSettingsStatus", "Test Telegram inviato. Controlla Telegram.");
  } catch (error) {
    phoenixSetText("phoenixSettingsStatus", "Test Telegram non riuscito. Verifica servizio notify, Chat ID e log di Home Assistant.");
  } finally {
    if (button) button.disabled = false;
  }
}

window.phoenixOpenSettings = phoenixOpenSettings;
window.phoenixCloseSettings = phoenixCloseSettings;

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
