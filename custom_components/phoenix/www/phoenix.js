const STATUS_URLS = [
  "/local/phoenix-ai-trader-ha/phoenix_status.json",
  "/local/phoenix-ai-trader-ha/status.json",
  "/local/phoenix-ai-trader/phoenix_status.json",
  "/local/phoenix-ai-trader/status.json"
];

const CONTACT_EMAIL = "pasquale.play4@gmail.com";
const PAYPAL_LINK = "https://paypal.me/PakyDJ/9.99EUR";
const LANG_KEY = "phoenixAiTraderLanguage";
let currentLang = localStorage.getItem(LANG_KEY) === "en" ? "en" : "it";
let lastData = null;
let lastLoadFailed = false;

const COINS = {
  BTC: ["Bitcoin", "₿"], ETH: ["Ethereum", "◆"], SOL: ["Solana", "◎"], BNB: ["BNB", "🟡"],
  XRP: ["XRP", "✕"], ADA: ["Cardano", "₳"], DOGE: ["Dogecoin", "Ð"], AVAX: ["Avalanche", "🔺"],
  LINK: ["Chainlink", "🔗"], DOT: ["Polkadot", "●"], LTC: ["Litecoin", "Ł"], MATIC: ["Polygon", "⬡"],
  POL: ["Polygon", "⬡"], ARB: ["Arbitrum", "🟠"], NEAR: ["NEAR Protocol", "🟣"], ATOM: ["Cosmos", "⚛️"],
  OP: ["Optimism", "🔴"], UNI: ["Uniswap", "🦄"], APT: ["Aptos", "🔵"], INJ: ["Injective", "⚡"],
  RUNE: ["THORChain", "ᚱ"]
};

const I18N = {
  it: {
    heroSubtitle: "Paper Trading con AI per Home Assistant",
    paperNotice: "🧪 Modalità Paper Trading — simulazione virtuale, nessun acquisto reale viene eseguito.",
    loading: "Caricamento dati Phoenix...",
    online: "Online",
    lastUpdate: "ultimo update",
    licenseActive: "Licenza attiva",
    demoExpired: "Demo scaduta",
    demo: "Demo",
    dataUnavailable: "Dati non disponibili",
    unableToRead: "🔴 Impossibile leggere i dati Phoenix",
    renderError: "🔴 Errore durante il rendering della dashboard Phoenix",
    renderCheck: "I dati sono stati letti, ma la dashboard ha incontrato un errore grafico. Aggiorna Phoenix e fai Ctrl+F5.",
    dataCheck: "Controlla che i file dati Phoenix siano raggiungibili da Home Assistant.",
    resetMission: "🔄 Reset missione",
    settings: "⚙️ Impostazioni Phoenix",
    insertLicense: "🔑 Inserisci licenza",
    updateLicense: "🔁 Aggiorna licenza",
    equity: "Equity",
    balance: "Liquidità",
    invested: "Investito",
    openPL: "P/L aperto",
    totalProfit: "Profitto totale",
    winRate: "Win rate",
    openTrades: "Trade aperti",
    demoLicense: "Demo/Licenza",
    accounting: "💼 Contabilità",
    openValue: "Valore posizioni",
    closedProfit: "Profitto chiuso",
    closedTrades: "Trade chiusi",
    licenseStatus: "Stato licenza",
    telegram: "Telegram",
    active: "Attivo",
    inactive: "Non attivo",
    license: "🔐 Licenza",
    status: "Stato",
    email: "Email associata",
    licenseExpiry: "Scadenza licenza",
    demoExpiry: "Scadenza demo",
    plan: "Piano",
    action: "Azione",
    missionProgress: "🎯 Avanzamento missione",
    missionTime: "Tempo missione",
    capitalTarget: "Capitale verso obiettivo",
    unavailableDuration: "durata non disponibile",
    missionEnded: "missione conclusa",
    daysLeft: "giorni rimasti",
    hoursLeft: "ore rimaste",
    gainedOnNeeded: (gained, needed, target) => `${gained} guadagnati su ${needed} necessari · Target ${target}`,
    phoenixRole: "🤖 Ruolo Phoenix",
    roleText: "Phoenix analizza il mercato crypto, apre posizioni virtuali automatiche e ti mostra se la strategia sta performando, prima di rischiare denaro reale.",
    mode: "Modalità",
    autoPaperTrader: "Paper Trader automatico",
    support: "Supporto",
    supportText: "privato e autonomo alla valutazione della strategia",
    waitingSetup: "in attesa setup",
    rule: "Regola",
    ruleText: score => `apre posizioni virtuali con score ≥ ${score}`,
    capitalPerTrade: "Capitale per trade",
    liquidityPercent: percent => `${percent}% della liquidità disponibile`,
    lastOperation: "Ultima operazione",
    noVirtualOperation: "Nessuna operazione virtuale ancora aperta",
    safety: "Sicurezza",
    noRealOrder: "nessun ordine reale eseguito",
    topSetup: "🏆 Top setup",
    coin: "Moneta",
    confidence: "Confidenza",
    quality: "Qualità",
    openPositions: "📈 Posizioni aperte",
    noPositions: "Nessuna posizione aperta.",
    amount: "Investito",
    value: "Valore",
    topMarket: "🔥 Top 20 mercato",
    noMarketData: "Nessun dato mercato disponibile.",
    lockedTitle: "⛔ Demo gratuita terminata",
    lockedIntro: "La prova gratuita di 24 ore è terminata. Per continuare a usare Phoenix AI Trader devi acquistare e inserire una licenza personale annuale.",
    launchOffer: "🔑 Offerta lancio 9,99 € · poi 19,99 €/anno",
    unlockedFeatures: "Con la licenza attiva sblocchi dashboard, sensori, Top 20 mercato, monitoraggio P/L e alert Telegram.",
    step1: "1. Acquista", step1Text: "Paga con PayPal usando l'offerta lancio.",
    step2: "2. Ricevi codice", step2Text: "La licenza firmata viene inviata via email.",
    step3: "3. Inserisci licenza", step3Text: "Apri Impostazioni Phoenix e incolla il codice.",
    currentState: "Stato attuale", configuredEmail: "Email configurata",
    paidRequest: "📩 Ho pagato, richiedo licenza",
    disclaimer: "⚠️ Phoenix è un supporto privato e autonomo alla valutazione di strategie in Paper Trading. Non fornisce consulenza finanziaria e non garantisce guadagni. Ogni decisione economica resta sotto responsabilità dell'utente.",
    notSet: "non impostata"
  },
  en: {
    heroSubtitle: "AI Paper Trading for Home Assistant",
    paperNotice: "🧪 Paper Trading mode — virtual simulation, no real purchase is executed.",
    loading: "Loading Phoenix data...",
    online: "Online",
    lastUpdate: "last update",
    licenseActive: "License active",
    demoExpired: "Demo expired",
    demo: "Demo",
    dataUnavailable: "Data unavailable",
    unableToRead: "🔴 Unable to read Phoenix data",
    renderError: "🔴 Error while rendering the Phoenix dashboard",
    renderCheck: "Data was loaded, but the dashboard hit a visual rendering error. Update Phoenix and press Ctrl+F5.",
    dataCheck: "Check that Phoenix data files are reachable from Home Assistant.",
    resetMission: "🔄 Reset mission",
    settings: "⚙️ Phoenix settings",
    insertLicense: "🔑 Enter license",
    updateLicense: "🔁 Update license",
    equity: "Equity",
    balance: "Balance",
    invested: "Invested",
    openPL: "Open P/L",
    totalProfit: "Total profit",
    winRate: "Win rate",
    openTrades: "Open trades",
    demoLicense: "Demo/License",
    accounting: "💼 Accounting",
    openValue: "Position value",
    closedProfit: "Closed profit",
    closedTrades: "Closed trades",
    licenseStatus: "License status",
    telegram: "Telegram",
    active: "Active",
    inactive: "Inactive",
    license: "🔐 License",
    status: "Status",
    email: "Associated email",
    licenseExpiry: "License expiry",
    demoExpiry: "Demo expiry",
    plan: "Plan",
    action: "Action",
    missionProgress: "🎯 Mission progress",
    missionTime: "Mission time",
    capitalTarget: "Capital toward target",
    unavailableDuration: "duration unavailable",
    missionEnded: "mission completed",
    daysLeft: "days left",
    hoursLeft: "hours left",
    gainedOnNeeded: (gained, needed, target) => `${gained} gained out of ${needed} needed · Target ${target}`,
    phoenixRole: "🤖 Phoenix role",
    roleText: "Phoenix analyzes the crypto market, opens automatic virtual positions and shows whether the strategy is performing before risking real money.",
    mode: "Mode",
    autoPaperTrader: "Automatic Paper Trader",
    support: "Support",
    supportText: "private and autonomous strategy evaluation",
    waitingSetup: "waiting for setup",
    rule: "Rule",
    ruleText: score => `opens virtual positions with score ≥ ${score}`,
    capitalPerTrade: "Capital per trade",
    liquidityPercent: percent => `${percent}% of available liquidity`,
    lastOperation: "Last operation",
    noVirtualOperation: "No virtual operation opened yet",
    safety: "Safety",
    noRealOrder: "no real order executed",
    topSetup: "🏆 Top setup",
    coin: "Coin",
    confidence: "Confidence",
    quality: "Quality",
    openPositions: "📈 Open positions",
    noPositions: "No open position.",
    amount: "Invested",
    value: "Value",
    topMarket: "🔥 Market Top 20",
    noMarketData: "No market data available.",
    lockedTitle: "⛔ Free demo ended",
    lockedIntro: "The 24-hour free trial has ended. To keep using Phoenix AI Trader, purchase and enter a personal annual license.",
    launchOffer: "🔑 Launch offer €9.99 · then €19.99/year",
    unlockedFeatures: "With an active license you unlock dashboard, sensors, Market Top 20, P/L monitoring and Telegram alerts.",
    step1: "1. Buy", step1Text: "Pay with PayPal using the launch offer.",
    step2: "2. Receive code", step2Text: "The signed license is sent by email.",
    step3: "3. Enter license", step3Text: "Open Phoenix settings and paste the code.",
    currentState: "Current status", configuredEmail: "Configured email",
    paidRequest: "📩 I paid, request license",
    disclaimer: "⚠️ Phoenix is a private and autonomous support tool for evaluating Paper Trading strategies. It is not financial advice and does not guarantee profits. Every financial decision remains the user's responsibility.",
    notSet: "not set"
  }
};

function locale() { return I18N[currentLang] || I18N.it; }
const t = key => locale()[key] ?? I18N.it[key] ?? key;
const money = value => `${Number(value || 0).toFixed(2)} €`;
const pct = value => `${Number(value || 0).toFixed(2)}%`;
const cls = value => Number(value || 0) >= 0 ? "good" : "bad";
const app = document.getElementById("app");
const statusEl = document.getElementById("status");
const pill = document.getElementById("licensePill");

function clamp(value, min = 0, max = 100) { return Math.max(min, Math.min(max, Number(value || 0))); }

function updateStaticText() {
  document.documentElement.lang = currentLang === "en" ? "en" : "it";
  const hero = document.getElementById("phoenixHeroSubtitle");
  const notice = document.getElementById("phoenixPaperNotice");
  const reset = document.getElementById("phoenixResetMissionBtn");
  const settings = document.getElementById("phoenixOpenSettingsBtn");
  const langIt = document.getElementById("phoenixLangIt");
  const langEn = document.getElementById("phoenixLangEn");
  if (hero) hero.textContent = t("heroSubtitle");
  if (notice) notice.textContent = t("paperNotice");
  if (reset) reset.textContent = t("resetMission");
  if (settings) settings.textContent = t("settings");
  if (statusEl && !lastData && !lastLoadFailed) statusEl.textContent = t("loading");
  if (statusEl && lastLoadFailed) statusEl.textContent = t("unableToRead");
  if (app && lastLoadFailed) app.innerHTML = `<div class="notice expired">${t("dataCheck")}</div>`;
  if (langIt) langIt.classList.toggle("active", currentLang === "it");
  if (langEn) langEn.classList.toggle("active", currentLang === "en");
}

function setLanguage(lang) {
  currentLang = lang === "en" ? "en" : "it";
  localStorage.setItem(LANG_KEY, currentLang);
  updateStaticText();
  if (lastData) renderLoadedData(lastData); else load();
}

function remainingText(seconds) {
  if (seconds === null || seconds === undefined) return "";
  const safe = Math.max(0, Number(seconds || 0));
  const hours = Math.floor(safe / 3600);
  const minutes = Math.floor((safe % 3600) / 60);
  return `${hours}h ${minutes}m`;
}

function licenseExpiryText(data) { return data.license_expires_at || data.license_expiry || data.demo_expires_at || "N/D"; }
function licenseEmailText(data) { return data.email || t("notSet"); }
function insertLicenseButton(label = t("insertLicense")) { return `<button class="btn" type="button" onclick="window.phoenixOpenSettings ? window.phoenixOpenSettings() : document.getElementById('phoenixOpenSettingsBtn')?.click()">${label}</button>`; }
function baseSymbol(symbol) { return String(symbol || "").replace("USDT", "").replace("BUSD", "").replace("FDUSD", "").replace("USDC", ""); }
function coinHtml(symbol) {
  const ticker = baseSymbol(symbol);
  const [name, logo] = COINS[ticker] || [ticker || "N/D", "🪙"];
  return `<div class="coin"><span class="logo">${logo}</span><div><div class="coin-name">${name}</div><div class="ticker">${ticker} · ${symbol || "N/D"}</div></div></div>`;
}

function parsePhoenixDate(value) {
  if (!value) return null;
  const parsed = new Date(String(value).replace(" ", "T"));
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function addMissionDuration(startDate, value, unit) {
  const end = new Date(startDate.getTime());
  const amount = Number(value || 0);
  if (unit === "hours") end.setHours(end.getHours() + amount);
  else if (unit === "weeks") end.setDate(end.getDate() + amount * 7);
  else if (unit === "months") end.setMonth(end.getMonth() + amount);
  else if (unit === "years") end.setFullYear(end.getFullYear() + amount);
  else end.setDate(end.getDate() + amount);
  return end;
}

function missionTimeProgress(data) {
  const mission = data.mission || {};
  const start = parsePhoenixDate(mission.start_date || data.created_at);
  const durationValue = Number(mission.duration_value || data.duration_value || 0);
  const durationUnit = mission.duration_unit || data.duration_unit || "days";
  if (!start || durationValue <= 0) return { percent: 0, label: t("unavailableDuration") };
  const end = addMissionDuration(start, durationValue, durationUnit);
  const totalMs = end.getTime() - start.getTime();
  const elapsedMs = Date.now() - start.getTime();
  if (totalMs <= 0) return { percent: 100, label: t("missionEnded") };
  const percent = clamp((elapsedMs / totalMs) * 100);
  const remainingMs = Math.max(0, end.getTime() - Date.now());
  const remainingHours = Math.floor(remainingMs / 3600000);
  const remainingDays = Math.floor(remainingHours / 24);
  const label = remainingDays > 0 ? `${remainingDays} ${t("daysLeft")}` : `${remainingHours} ${t("hoursLeft")}`;
  return { percent, label };
}

function progressBar(title, percent, detail, icon = "📊") {
  const safe = clamp(percent);
  return `<div style="margin:14px 0 18px"><div style="display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:8px"><strong>${icon} ${title}</strong><span class="small">${safe.toFixed(1)}%</span></div><div style="height:14px;background:rgba(15,23,42,.9);border:1px solid rgba(148,163,184,.28);border-radius:999px;overflow:hidden"><div style="height:100%;width:${safe}%;background:linear-gradient(90deg,#38bdf8,#22c55e);border-radius:999px"></div></div><p class="small" style="margin:7px 0 0">${detail}</p></div>`;
}

function setPill(data) {
  if (data.license_status === "active") { pill.className = "pill active"; pill.textContent = `✅ ${t("licenseActive")}`; return; }
  if (data.locked || data.demo_expired || ["expired", "invalid"].includes(data.license_status)) { pill.className = "pill expired"; pill.textContent = `⛔ ${t("demoExpired")}`; return; }
  pill.className = "pill trial";
  pill.textContent = `⏳ ${t("demo")} ${remainingText(data.demo_remaining_seconds)}`;
}

function card(label, value, css = "accent") { return `<div class="card"><div class="label">${label}</div><div class="value ${css}">${value}</div></div>`; }
function rows(items) { return `<table>${items.map(item => `<tr><th>${item[0]}</th><td class="${item[2] || ""}">${item[1]}</td></tr>`).join("")}</table>`; }

function renderLocked(data) {
  const subject = encodeURIComponent("Phoenix AI Trader License");
  const body = encodeURIComponent(`Hello, I purchased the Phoenix AI Trader license with PayPal.\n\nHome Assistant/PayPal email: ${data.email || ""}\nLicense status: ${data.license_status || "expired"}`);
  app.innerHTML = `<section class="locked"><div class="locked-box"><h2>${t("lockedTitle")}</h2><p><b>${t("lockedIntro")}</b></p><div class="license-badge">${t("launchOffer")}</div><p>${t("roleText")}</p><p>${t("unlockedFeatures")}</p><div class="steps"><div class="step"><b>${t("step1")}</b><br><span class="small">${t("step1Text")}</span></div><div class="step"><b>${t("step2")}</b><br><span class="small">${t("step2Text")}</span></div><div class="step"><b>${t("step3")}</b><br><span class="small">${t("step3Text")}</span></div></div><p class="small">${t("currentState")}: ${data.license_status || "expired"} · ${t("configuredEmail")}: ${licenseEmailText(data)} · ${t("demoExpiry")}: ${data.demo_expires_at || "N/D"}</p><a class="btn btn-pay" href="${PAYPAL_LINK}" target="_blank" rel="noopener">💳 ${currentLang === "en" ? "Buy license €9.99" : "Acquista licenza 9,99 €"}</a>${insertLicenseButton()}<a class="btn" href="mailto:${CONTACT_EMAIL}?subject=${subject}&body=${body}">${t("paidRequest")}</a><p class="small">${t("disclaimer")}</p></div></section>`;
}

function renderLicensePanel(data) {
  const active = data.license_status === "active";
  const status = active ? t("active") : (data.demo_expired || data.locked ? t("demoExpired") : `${t("demo")} ${t("active")}`);
  const css = active ? "good" : (data.demo_expired || data.locked ? "bad" : "warn");
  return `<div class="card wide"><h2>${t("license")}</h2>${rows([[t("status"), status, css],[t("email"), licenseEmailText(data)],[active ? t("licenseExpiry") : t("demoExpiry"), licenseExpiryText(data)],[t("plan"), data.license_plan || (active ? "Annual" : "Trial")],[t("action"), insertLicenseButton(active ? t("updateLicense") : t("insertLicense"))]])}</div>`;
}

function renderMissionProgressPanel(data) {
  const time = missionTimeProgress(data);
  const capitalProgress = clamp(data.target_progress_percent);
  const start = Number(data.start_balance || data.mission?.start_capital || 0);
  const target = Number(data.target_capital || data.mission?.target_capital || 0);
  const equity = Number(data.equity || 0);
  const gained = Math.max(0, equity - start);
  const needed = Math.max(0, target - start);
  return `<div class="card full"><h2>${t("missionProgress")}</h2>${progressBar(t("missionTime"), time.percent, time.label, "⏱️")}${progressBar(t("capitalTarget"), capitalProgress, locale().gainedOnNeeded(money(gained), money(needed), money(target)), "💰")}</div>`;
}

function renderPaperTraderPanel(data) {
  const status = data.paper_trader_status || t("waitingSetup");
  const lastTrade = data.last_trade && data.last_trade !== "N/D" ? data.last_trade : t("noVirtualOperation");
  const allocation = data.auto_trade_allocation_percent ? locale().liquidityPercent(Number(data.auto_trade_allocation_percent).toFixed(0)) : locale().liquidityPercent(25);
  const minScore = data.auto_trade_min_score || 80;
  return `<div class="card wide"><h2>${t("phoenixRole")}</h2><p class="small">${t("roleText")}</p>${rows([[t("mode"), t("autoPaperTrader"), "good"],[t("support"), t("supportText")],[t("status"), status],[t("rule"), locale().ruleText(minScore)],[t("capitalPerTrade"), allocation],[t("lastOperation"), lastTrade],[t("safety"), t("noRealOrder"), "warn"]])}</div>`;
}

function renderDashboard(data) {
  const profit = Number(data.total_profit || 0);
  const unrealized = Number(data.unrealized_pnl || 0);
  app.innerHTML = `<section class="grid">${card(t("equity"), money(data.equity), cls(profit))}${card(t("balance"), money(data.balance), "accent")}${card(t("invested"), money(data.invested_amount), "warn")}${card(t("openPL"), `${money(unrealized)} · ${pct(data.unrealized_pnl_percent)}`, cls(unrealized))}${card(t("totalProfit"), `${money(data.total_profit)} · ${pct(data.total_profit_percent)}`, cls(profit))}${card(t("winRate"), pct(data.win_rate), "accent")}${card(t("openTrades"), data.open_positions || 0, "accent")}${card(t("demoLicense"), data.license_status === "active" ? t("licenseActive") : remainingText(data.demo_remaining_seconds), data.license_status === "active" ? "good" : "warn")}${renderMissionProgressPanel(data)}<div class="card wide"><h2>${t("accounting")}</h2>${rows([[t("openValue"), money(data.open_value)],[t("closedProfit"), money(data.closed_profit)],[t("closedTrades"), data.closed_trades || 0],[t("licenseStatus"), data.license_status || "demo"],[t("telegram"), data.telegram_enabled ? t("active") : t("inactive"), data.telegram_enabled ? "good" : "warn"]])}</div>${renderPaperTraderPanel(data)}${renderLicensePanel(data)}<div class="card wide"><h2>${t("topSetup")}</h2>${rows([[t("coin"), coinHtml(data.top_crypto)],["Score", data.top_score ?? "--"],[t("confidence"), data.top_confidence || "N/D"],[t("quality"), data.top_quality || "N/D"]])}</div><div class="card full"><h2>${t("openPositions")}</h2>${positionsTable(data.positions || [])}</div><div class="card full"><h2>${t("topMarket")}</h2>${topTable(data.top20 || [])}</div></section>`;
}

function positionsTable(items) {
  if (!items.length) return `<p class="small">${t("noPositions")}</p>`;
  return `<table><tr><th>${t("coin")}</th><th>${t("amount")}</th><th>${t("value")}</th><th>P/L</th><th>Score</th></tr>${items.map(item => `<tr><td>${coinHtml(item.symbol)}</td><td>${money(item.amount)}</td><td>${money(item.current_value)}</td><td class="${cls(item.pnl)}">${money(item.pnl)} · ${pct(item.change_percent)}</td><td>${item.score ?? "--"}</td></tr>`).join("")}</table>`;
}

function topTable(items) {
  if (!items.length) return `<p class="small">${t("noMarketData")}</p>`;
  return `<table><tr><th>#</th><th>${t("coin")}</th><th>Score</th><th>Conf.</th><th>RSI</th><th>1h</th></tr>${items.map((item, index) => `<tr><td>${index + 1}</td><td>${coinHtml(item.symbol)}</td><td>${item.score ?? "--"}</td><td>${item.confidence ?? "--"}</td><td>${item.rsi ?? "--"}</td><td class="${cls(item.change_1h)}">${pct(item.change_1h)}</td></tr>`).join("")}</table>`;
}

async function fetchStatus() {
  for (const url of STATUS_URLS) {
    try {
      const response = await fetch(`${url}?ts=${Date.now()}`);
      if (response.ok) return await response.json();
    } catch (error) { console.debug("Phoenix status fetch failed", url, error); }
  }
  throw new Error("Phoenix status file not found");
}

function renderDashboardOrLocked(data) {
  if (data.locked || data.demo_expired || ["expired", "invalid"].includes(data.license_status)) renderLocked(data); else renderDashboard(data);
}

function renderLoadedData(data) {
  lastLoadFailed = false;
  try {
    setPill(data);
    statusEl.textContent = `🟢 ${t("online")} · v${data.version || "--"} · ${t("lastUpdate")} ${data.last_update || "--"}`;
    renderDashboardOrLocked(data);
  } catch (error) {
    console.error("Phoenix dashboard render error", error);
    pill.className = "pill expired";
    pill.textContent = t("dataUnavailable");
    statusEl.textContent = t("renderError");
    app.innerHTML = `<div class="notice expired">${t("renderCheck")}</div>`;
  }
}

async function load() {
  try {
    const data = await fetchStatus();
    lastData = data;
    renderLoadedData(data);
  } catch (error) {
    console.error("Phoenix status load error", error);
    lastData = null;
    lastLoadFailed = true;
    pill.className = "pill expired";
    pill.textContent = t("dataUnavailable");
    statusEl.textContent = t("unableToRead");
    app.innerHTML = `<div class="notice expired">${t("dataCheck")}</div>`;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const langIt = document.getElementById("phoenixLangIt");
  const langEn = document.getElementById("phoenixLangEn");
  if (langIt) langIt.addEventListener("click", () => setLanguage("it"));
  if (langEn) langEn.addEventListener("click", () => setLanguage("en"));
  updateStaticText();
});

window.phoenixSetLanguage = setLanguage;
updateStaticText();
load();
setInterval(load, 30000);
