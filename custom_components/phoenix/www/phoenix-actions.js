function phoenixAuthHeaders() {
  try {
    const raw = localStorage.getItem("hassTokens");
    const token = raw ? JSON.parse(raw).access_token : null;
    return token ? { Authorization: `Bearer ${token}` } : {};
  } catch (error) {
    return {};
  }
}

async function phoenixResetMission() {
  const ok = confirm("Vuoi resettare la missione Phoenix? Capitale, tempo e statistiche paper trading torneranno ai valori configurati.");
  if (!ok) return;

  const button = document.getElementById("phoenixResetMissionBtn");
  if (button) button.disabled = true;

  try {
    const response = await fetch("/api/phoenix/reset_mission", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        ...phoenixAuthHeaders(),
      },
      body: "{}",
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    alert("Missione Phoenix resettata.");
    if (typeof load === "function") {
      await load();
    } else {
      window.location.reload();
    }
  } catch (error) {
    alert("Reset non riuscito. Riprova dopo il riavvio di Home Assistant o usa Configura dall'integrazione Phoenix.");
  } finally {
    if (button) button.disabled = false;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const resetButton = document.getElementById("phoenixResetMissionBtn");
  if (resetButton) resetButton.addEventListener("click", phoenixResetMission);
});
