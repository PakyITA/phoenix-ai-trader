<div align="center">

<img src="docs/logo.png" width="180" alt="Phoenix AI Trader Logo">

# 🦅 Phoenix AI Trader

### AI-powered Paper Trading for Home Assistant

**Simulate your crypto portfolio. Track profit and loss. Learn without risking real money.**

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1+-41BDF5?style=for-the-badge)
![Trial](https://img.shields.io/badge/Trial-24h-orange?style=for-the-badge)
![Launch Offer](https://img.shields.io/badge/Launch%20Offer-9.99%E2%82%AC-orange?style=for-the-badge)
![Version](https://img.shields.io/badge/version-0.3.3-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-commercial-red?style=for-the-badge)

[![Add to Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PakyITA&repository=phoenix-ai-trader&category=integration)

**🇮🇹 Italian documentation:** [README.it.md](README.it.md)

---

**Phoenix AI Trader** brings a premium **Paper Trading experience** directly into **Home Assistant**.

Create a virtual crypto portfolio, monitor profit and loss, receive Telegram alerts and follow a personal capital mission — all without connecting to an exchange or risking real money.

> ⚠️ **Phoenix AI Trader is designed exclusively for Paper Trading.**
>
> It never connects to Binance, Bybit, Coinbase or any other exchange and never places real orders.

</div>

---

## 🚀 How Phoenix works

1. Install Phoenix from HACS.
2. Complete the setup wizard.
3. Use the full 24-hour free trial.
4. After the trial, Phoenix requires a personal license.
5. Purchase your license via PayPal.
6. Receive your signed license by email.
7. Paste the license in **Phoenix AI Trader → Configure**.

---

## 🔑 Free Trial & License

Phoenix AI Trader includes a **24-hour free trial**.

After the trial expires, the main dashboard and portfolio sensors are locked until a valid license is configured.

### 💥 Launch offer

For the first **15 days**, the personal Phoenix AI Trader license is available for:

```text
9.99 € instead of 19.99 €
```

After the launch offer ends, the standard license price is **19.99 €**.

Licenses are:

- linked to the buyer's PayPal email
- personal and non-transferable
- valid for one Home Assistant installation
- verified locally using a signed offline license

To buy a license, contact the developer after installation or use the PayPal instructions shown in the Phoenix dashboard when the trial expires.

---

## ✨ What makes Phoenix different

| | |
|---|---|
| 🧠 **AI Paper Trading** | Simulate a crypto portfolio and test ideas without risking real money |
| 📊 **Home Assistant dashboard** | Monitor equity, liquidity, open positions, profit/loss and mission progress |
| 📱 **Telegram alerts** | Receive alerts when simulated profit or loss crosses your thresholds |
| 🎯 **Mission Mode** | Set an initial capital, target capital and time goal |
| 🏠 **Native entities** | Use sensors and binary sensors in dashboards, scripts and automations |
| 🔐 **24h trial + license** | Try Phoenix first, then unlock it with a personal signed license |
| 🧩 **No YAML required** | Full setup through the Home Assistant integration wizard |

---

## 📊 Dashboard Preview

Phoenix includes a dedicated Home Assistant sidebar panel with:

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

## 🏠 Home Assistant Entities

Phoenix creates native Home Assistant entities such as:

### Sensors

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

### Binary sensors

- License active
- Trial active
- Phoenix locked
- Telegram enabled

These entities can be used in dashboards, automations, scripts and notifications.

---

## ⚙️ Setup Wizard

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

## 🧾 Changing License or Settings

Phoenix supports the Home Assistant **Configure** button.

Go to:

```text
Settings → Devices & services → Phoenix AI Trader → Configure
```

From there you can update:

- license email
- activation code
- Telegram notifications
- alert thresholds
- mission settings

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

### Method 1 — Add to Home Assistant

Click the **Add to Home Assistant** badge at the top of this README.

### Method 2 — Manual custom repository

1. Open HACS
2. Go to **Integrations**
3. Add this repository as a custom repository
4. Select category **Integration**
5. Install **Phoenix AI Trader**
6. Restart Home Assistant
7. Go to **Settings → Devices & services**
8. Add **Phoenix AI Trader**
9. Complete the setup wizard

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

## 💬 Support

| | |
|---|---|
| 🐛 **Bugs** | Open a GitHub Issue |
| 💡 **Ideas** | Use GitHub Discussions or contact the developer |
| 🔑 **License** | Launch offer: **9.99 € for 15 days**, then **19.99 €** · PayPal purchase → signed license by email |
| 🇮🇹 **Italian support** | Italian documentation available in [README.it.md](README.it.md) |

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
