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
        <h2>🚀 Continua con Phoenix AI Trader</h2>
        <p>Phoenix ha completato la demo gratuita di 24 ore.</p>
        <div class="license-badge">🔑 Offerta lancio 9,99 € · poi 19,99 €</div>
        <p>Per continuare a usare dashboard, sensori, monitoraggio P/L e alert Telegram, acquista una licenza personale. Dopo il pagamento riceverai un codice licenza firmato da inserire in Home Assistant.</p>
        <div class="steps">
          <div class="step"><b>1. Paga con PayPal</b><br><span class="small">Offerta lancio: 9,99 € per 15 giorni.</span></div>
          <div class="step"><b>2. Invia conferma</b><br><span class="small">Usa l'email PayPal/Home Assistant per ricevere il codice.</span></div>
          <div class="step"><b>3. Attiva Phoenix</b><br><span class="small">Vai su Phoenix AI Trader → Configura e incolla il codice.</span></div>
        </div>
        <p class="small">Stato attuale: ${data.license_status || "expired"} · Email configurata: ${data.email || "non impostata"}</p>
        <a class="btn btn-pay" href="${PAYPAL_LINK}" target="_blank" rel="noopener">💳 ${PAYPAL_TEXT}</a>
        <a class="btn" href="mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}">📩 Ho pagato, richiedo licenza</a>
        <a class="btn" href="/config/integrations">⚙️ Apri integrazioni</a>
      </div>
    </section>`;
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
      ${card("Demo residua", remainingText(data.demo_remaining_seconds) || "Licenza attiva", data.license_status === "active" ? "good" : "warn")}
      <div class="card wide"><h2>💼 Contabilità</h2>${rows([
        ["Valore posizioni", money(data.open_value)],
        ["Profitto chiuso", money(data.closed_profit)],
        ["Trade chiusi", data.closed_trades || 0],
        ["Stato licenza", data.license_status || "demo"],
        ["Telegram", data.telegram_enabled ? "Attivo" : "Non attivo", data.telegram_enabled ? "good" : "warn"]
      ])}</div>
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
