<div align="center">

<img src="docs/logo.png" width="180" alt="Phoenix AI Trader Logo">

# 🦅 Phoenix AI Trader

### AI-powered Paper Trading for Home Assistant

**Simulate • Learn • Improve**

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1+-41BDF5?style=for-the-badge)
![Trial](https://img.shields.io/badge/Trial-24h-orange?style=for-the-badge)
![Version](https://img.shields.io/badge/version-0.3.2-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-commercial-red?style=for-the-badge)

**🇮🇹 Italian documentation:** [README.it.md](README.it.md)

---

**Phoenix AI Trader** brings an advanced **Paper Trading platform** directly into **Home Assistant**.

Test trading strategies, monitor a virtual portfolio, track performance and improve your decision-making without risking real money.

> ⚠️ **Phoenix AI Trader is designed exclusively for Paper Trading.**
>
> It never connects to cryptocurrency exchanges and never places real orders.

</div>

---

## ✨ Features

### 🧠 AI Paper Trading

Create and manage a completely virtual cryptocurrency portfolio.

Perfect for:

- Learning trading concepts
- Testing new strategies
- Improving discipline
- Monitoring simulated performance
- Building Home Assistant automations around portfolio events

---

### 📊 Professional Dashboard

Phoenix includes an integrated Home Assistant dashboard with:

- 💰 Portfolio value
- 📈 Equity
- 📉 Profit / Loss
- 🎯 Mission progress
- 🏆 Top opportunities
- 📊 Win rate
- 🪙 Cryptocurrency logos
- 🧠 AI score
- 🔐 Trial / license status

<p align="center">
  <img src="docs/dashboard.png" width="95%" alt="Phoenix AI Trader Dashboard Preview">
</p>

---

### 🏠 Native Home Assistant Integration

Phoenix creates native Home Assistant entities such as:

- Equity
- Balance
- Invested amount
- Open value
- Open profit / loss
- Total profit
- Total profit percentage
- Win rate
- Open positions
- Closed trades
- Top cryptocurrency
- Last update
- License status
- Remaining trial time

These entities can be used in dashboards, automations, scripts and notifications.

---

### ⚙️ Automatic Setup Wizard

After installation, configure Phoenix from:

```text
Settings → Devices & services → Add integration → Phoenix AI Trader
```

During the setup wizard you can configure:

- Data folder
- Initial capital
- Target capital
- Mission duration
- Email
- Optional activation code
- Optional Telegram notifications
- Profit / loss alert threshold in EUR
- Profit / loss alert threshold in percent
- Alert cooldown time

No manual YAML configuration is required.

---

## ⏳ 24-hour Trial

Phoenix AI Trader includes a complete local 24-hour trial.

During the trial, users can test the full dashboard and sensors. When the trial expires, Phoenix can lock the main dashboard and sensors until a valid activation code is configured.

> Note: the current trial system is local/offline. Without an online license backend, a determined technical user may still bypass local checks.

---

## 🎯 Mission Mode

Set your personal investment challenge.

Configure:

- Initial capital
- Target capital
- Duration

Phoenix automatically tracks:

- Capital progress
- Time progress
- Goal completion

---

## 📱 Telegram Notifications

Phoenix can send Home Assistant `notify` alerts when the simulated portfolio reaches a configured profit or loss threshold.

Example service:

```text
notify.telegram
```

If your Home Assistant Telegram notification service has a different name, enter it in the setup wizard.

---

## 📦 Installation with HACS

1. Open HACS
2. Go to **Integrations**
3. Add this repository as a custom repository
4. Install **Phoenix AI Trader**
5. Restart Home Assistant
6. Go to **Settings → Devices & services**
7. Add **Phoenix AI Trader**
8. Complete the setup wizard

---

## 📁 Default Data Folder

```text
/config/phoenix-ai-trader-ha
```

The integration automatically generates all required files inside this folder.

---

## 🔒 Safety

Phoenix AI Trader is **100% Paper Trading**.

It:

✅ Never connects to Binance  
✅ Never connects to Bybit  
✅ Never connects to Coinbase  
✅ Never executes real trades  
✅ Never manages your funds  
✅ Never requires exchange API keys  

Everything is simulated locally inside Home Assistant.

---

## 📡 Planned Features

Upcoming releases may include:

- 📱 Advanced Telegram notifications
- 📈 Profit / loss alerts
- 🤖 AI trading assistant
- 📊 Interactive charts
- 📄 PDF reports
- 📈 Strategy comparison
- 🧠 AI trade explanations
- 🌍 Multi-portfolio support
- 📚 Trading statistics
- 📉 Historical analytics
- 🔐 Online license backend

---

## 📜 License

Phoenix AI Trader is proprietary commercial software.

A valid license grants personal, non-transferable use on the purchaser's own Home Assistant instance.

Redistribution, resale, sublicensing, publishing modified copies, or making the software available to third parties is not allowed without written permission.

---

<div align="center">

## 🦅 Phoenix AI Trader

**AI-powered Paper Trading for Home Assistant.**

Built with ❤️ by PakyITA.

</div>
