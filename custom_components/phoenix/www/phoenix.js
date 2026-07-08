const STATUS_URLS = [
  "/local/phoenix-ai-trader-ha/phoenix_status.json",
  "/local/phoenix-ai-trader/phoenix_status.json",
  "/local/phoenix-ai-trader/status.json"
];

const CONTACT_EMAIL = "pasquale.play4@gmail.com";
const PAYPAL_LINK = "https://paypal.me/PakyDJ/9.99EUR";
const PAYPAL_TEXT = "Acquista licenza 9,99 €";

const COINS = {
  BTC: ["Bitcoin", "₿"], ETH: ["Ethereum", "◆"], SOL: ["Solana", "◎"],
  BNB: ["BNB", "🟡"], XRP: ["XRP", "✕"], ADA: ["Cardano", "₳"],
  DOGE: ["Dogecoin", "Ð"], AVAX: ["Avalanche", "🔺"], LINK: ["Chainlink", "🔗"],
  DOT: ["Polkadot", "●"], LTC: ["Litecoin", "Ł"], MATIC: ["Polygon", "⬡"], POL: ["Polygon", "⬡"]
};

const money = value => `${Number(value || 0).toFixed(2)} €`;
const pct = value => `${Number(value || 0).toFixed(2)}%`;
const cls = value => Number(value || 0) >= 0 ? "good" : "bad";
const app = document.getElementById("app");
const statusEl = document.getElementById("status");
const pill = document.getElementById("licensePill");

function remainingText(seconds) {
  if (seconds === null || seconds === undefined) return "";
  const safe = Math.max(0, Number(seconds || 0));
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  return `${hours}h ${minutes}m`;
}

function licenseExpiryText(data) {
  return data.license_expires_at || data.license_expiry || data.demo_expires_at || "N/D";
}

function licenseEmailText(data) {
  return data.email || "non impostata";
}

function insertLicenseButton(label = "🔑 Inserisci licenza") {
  return `<button class="btn" type="button" onclick="window.phoenixOpenSettings ? window.phoenixOpenSettings() : document.getElementById('phoenixOpenSettingsBtn')?.click()">${label}</button>`;
}

function baseSymbol(symbol) {
  return String(symbol || "").replace("USDT", "").replace("BUSD", "").replace("FDUSD", "").replace("USDC", "");
}

function coinHtml(symbol) {
  const ticker = baseSymbol(symbol);
  const [name, logo] = COINS[ticker] || [ticker || "N/D", "🪙"];
  return `<div class="coin"><span class="logo">${logo}</span><div><div class="coin-name">${name}</div><div class="ticker">${ticker} · ${symbol || "N/D"}</div></div></div>`;
}

function setPill(data) {
  if (data.license_status === "active") {
    pill.className = "pill active";
    pill.textContent = "✅ Licenza attiva";
    return;
  }
  if (data.locked || data.demo_expired || ["expired", "invalid"].includes(data.license_status)) {
    pill.className = "pill expired";
    pill.textContent = "⛔ Demo scaduta";
    return;
  }
  pill.className = "pill trial";
  pill.textContent = `⏳ Demo ${remainingText(data.demo_remaining_seconds)}`;
}

function card(label, value, css = "accent") {
  return `<div class="card"><div class="label">${label}</div><div class="value ${css}">${value}</div></div>`;
}

function rows(items) {
  return `<table>${items.map(item => `<tr><th>${item[0]}</th><td class="${item[2] || ""}">${item[1]}</td></tr>`).join("")}</table>`;
}

function renderLocked(data) {
  const subject = encodeURIComponent("Licenza Phoenix AI Trader");
  const body = encodeURIComponent(`Ciao, ho acquistato la licenza Phoenix AI Trader da PayPal.\n\nEmail Home Assistant/PayPal: ${data.email || ""}\nStato licenza: ${data.license_status || "expired"}`);
  app.innerHTML = `
    <section class="locked">
      <div class="locked-box">
        <h2>⛔ Demo gratuita terminata</h2>
        <p><b>La prova gratuita di 24 ore è terminata.</b> Per continuare a usare Phoenix AI Trader devi acquistare e inserire una licenza personale annuale.</p>
        <div class="license-badge">🔑 Offerta lancio 9,99 € · poi 19,99 €/anno</div>
        <p>Con la licenza attiva sblocchi dashboard, sensori, Top 20 mercato, monitoraggio P/L e alert Telegram.</p>
        <div class="steps">
          <div class="step"><b>1. Acquista</b><br><span class="small">Paga con PayPal usando l'offerta lancio.</span></div>
          <div class="step"><b>2. Ricevi codice</b><br><span class="small">La licenza firmata viene inviata via email.</span></div>
          <div class="step"><b>3. Inserisci licenza</b><br><span class="small">Apri Impostazioni Phoenix e incolla il codice.</span></div>
        </div>
        <p class="small">Stato attuale: ${data.license_status || "expired"} · Email configurata: ${licenseEmailText(data)} · Scadenza demo: ${data.demo_expires_at || "N/D"}</p>
        <a class="btn btn-pay" href="${PAYPAL_LINK}" target="_blank" rel="noopener">💳 ${PAYPAL_TEXT}</a>
        ${insertLicenseButton()}
        <a class="btn" href="mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}">📩 Ho pagato, richiedo licenza</a>
        <p class="small">⚠️ Phoenix è solo Paper Trading e non fornisce consulenza finanziaria. Ogni decisione economica resta sotto responsabilità dell'utente.</p>
      </div>
    </section>`;
}

function renderLicensePanel(data) {
  const active = data.license_status === "active";
  const status = active ? "Attiva" : (data.demo_expired || data.locked ? "Demo scaduta" : "Demo attiva");
  const css = active ? "good" : (data.demo_expired || data.locked ? "bad" : "warn");
  return `<div class="card wide"><h2>🔐 Licenza</h2>${rows([
    ["Stato", status, css],
    ["Email associata", licenseEmailText(data)],
    [active ? "Scadenza licenza" : "Scadenza demo", licenseExpiryText(data)],
    ["Piano", data.license_plan || (active ? "Annual" : "Trial")],
    ["Azione", insertLicenseButton(active ? "🔁 Aggiorna licenza" : "🔑 Inserisci licenza")]
  ])}</div>`;
}

function renderDashboard(data) {
  const profit = Number(data.total_profit || 0);
  const unrealized = Number(data.unrealized_pnl || 0);
  app.innerHTML = `
    <section class="grid">
      ${card("Equity", money(data.equity), cls(profit))}
      ${card("Liquidità", money(data.balance), "accent")}
      ${card("Investito", money(data.invested_amount), "warn")}
      ${card("P/L aperto", `${money(unrealized)} · ${pct(data.unrealized_pnl_percent)}`, cls(unrealized))}
      ${card("Profitto totale", `${money(data.total_profit)} · ${pct(data.total_profit_percent)}`, cls(profit))}
      ${card("Win rate", pct(data.win_rate), "accent")}
      ${card("Trade aperti", data.open_positions || 0, "accent")}
      ${card("Demo/Licenza", data.license_status === "active" ? "Licenza attiva" : remainingText(data.demo_remaining_seconds), data.license_status === "active" ? "good" : "warn")}
      <div class="card wide"><h2>💼 Contabilità</h2>${rows([
        ["Valore posizioni", money(data.open_value)],
        ["Profitto chiuso", money(data.closed_profit)],
        ["Trade chiusi", data.closed_trades || 0],
        ["Stato licenza", data.license_status || "demo"],
        ["Telegram", data.telegram_enabled ? "Attivo" : "Non attivo", data.telegram_enabled ? "good" : "warn"]
      ])}</div>
      ${renderLicensePanel(data)}
      <div class="card wide"><h2>🏆 Top setup</h2>${rows([
        ["Moneta", coinHtml(data.top_crypto)],
        ["Score", data.top_score ?? "--"],
        ["Confidenza", data.top_confidence || "N/D"],
        ["Qualità", data.top_quality || "N/D"]
      ])}</div>
      <div class="card full"><h2>📈 Posizioni aperte</h2>${positionsTable(data.positions || [])}</div>
      <div class="card full"><h2>🔥 Top 20 mercato</h2>${topTable(data.top20 || [])}</div>
    </section>`;
}

function positionsTable(items) {
  if (!items.length) return `<p class="small">Nessuna posizione aperta.</p>`;
  return `<table><tr><th>Moneta</th><th>Investito</th><th>Valore</th><th>P/L</th><th>Score</th></tr>${items.map(item => `<tr><td>${coinHtml(item.symbol)}</td><td>${money(item.amount)}</td><td>${money(item.current_value)}</td><td class="${cls(item.pnl)}">${money(item.pnl)} · ${pct(item.change_percent)}</td><td>${item.score ?? "--"}</td></tr>`).join("")}</table>`;
}

function topTable(items) {
  if (!items.length) return `<p class="small">Nessun dato mercato disponibile.</p>`;
  return `<table><tr><th>#</th><th>Moneta</th><th>Score</th><th>Conf.</th><th>RSI</th><th>1h</th></tr>${items.map((item, index) => `<tr><td>${index + 1}</td><td>${coinHtml(item.symbol)}</td><td>${item.score ?? "--"}</td><td>${item.confidence ?? "--"}</td><td>${item.rsi ?? "--"}</td><td class="${cls(item.change_1h)}">${pct(item.change_1h)}</td></tr>`).join("")}</table>`;
}

async function fetchStatus() {
  for (const url of STATUS_URLS) {
    try {
      const response = await fetch(`${url}?ts=${Date.now()}`);
      if (response.ok) return await response.json();
    } catch (error) {}
  }
  throw new Error("Phoenix status file not found");
}

async function load() {
  try {
    const data = await fetchStatus();
    setPill(data);
    statusEl.textContent = `🟢 Online · v${data.version || "--"} · ultimo update ${data.last_update || "--"}`;
    if (data.locked || data.demo_expired || ["expired", "invalid"].includes(data.license_status)) {
      renderLocked(data);
    } else {
      renderDashboard(data);
    }
  } catch (error) {
    pill.className = "pill expired";
    pill.textContent = "Dati non disponibili";
    statusEl.textContent = "🔴 Impossibile leggere i dati Phoenix";
    app.innerHTML = `<div class="notice expired">Controlla che i file dati Phoenix siano raggiungibili da Home Assistant.</div>`;
  }
}

load();
setInterval(load, 30000);
