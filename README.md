<div align="center">

<img src="docs/logo.png" width="180" alt="Phoenix AI Trader Logo">

# 🦅 Phoenix AI Trader

### AI-powered Paper Trading for Home Assistant

**Simulate your crypto portfolio. Track profit and loss. Learn without risking real money.**

![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.1+-41BDF5?style=for-the-badge)
![Trial](https://img.shields.io/badge/Trial-24h-orange?style=for-the-badge)
![Annual License](https://img.shields.io/badge/License-Annual-red?style=for-the-badge)
![Launch Offer](https://img.shields.io/badge/Launch%20Offer-9.99%E2%82%AC-orange?style=for-the-badge)
![Version](https://img.shields.io/badge/version-0.4.1-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-commercial-red?style=for-the-badge)

[![Add to Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=PakyITA&repository=phoenix-ai-trader&category=integration)

**🇮🇹 Italian documentation:** [README.it.md](README.it.md)  
**📜 Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

**Phoenix AI Trader** brings a premium **Paper Trading experience** directly into **Home Assistant**.

Create a virtual crypto portfolio, monitor profit and loss, receive Telegram alerts and follow a personal capital mission — all without connecting to an exchange or risking real money.

> ⚠️ **Phoenix AI Trader is designed exclusively for Paper Trading.**
>
> It never connects to Binance, Bybit, Coinbase or any other exchange and never places real orders.

</div>

---

## ✅ Current Version

```text
0.4.1
```

### Highlights in 0.4.1

- Fixed Telegram MarkdownV2 parsing errors.
- Telegram alerts now escape reserved MarkdownV2 characters automatically.
- Automatic paper trading Telegram messages now work with Home Assistant Telegram notify services.
- Internal Phoenix version is aligned with the HACS manifest version.
- Improved Telegram troubleshooting instructions.

See the full changelog: [CHANGELOG.md](CHANGELOG.md)

---

## 🚀 How Phoenix works

1. Install Phoenix from HACS.
2. Complete the setup wizard.
3. Use the full 24-hour free trial.
4. After the trial, Phoenix requires a personal annual license.
5. Purchase your license via PayPal.
6. Receive your signed license by email.
7. Paste the license in **Phoenix AI Trader → Configure** or inside the Phoenix settings panel.

---

## 🔑 Free Trial & Annual License

Phoenix AI Trader includes a **24-hour free trial**.

After the trial expires, the main dashboard and portfolio sensors are locked until a valid license is configured.

Phoenix licenses are **annual**. A valid license unlocks Phoenix for **12 months from the issue date**. After the annual period ends, the license must be renewed to keep using the premium features.

### 💥 Launch offer

For the first **15 days**, the personal annual Phoenix AI Trader license is available for:

```text
9.99 € instead of 19.99 €
```

After the launch offer ends, the standard annual license price is **19.99 €**.

👉 **Buy the launch license:** https://paypal.me/PakyDJ/9.99EUR

Licenses are:

- annual and valid for 12 months from the issue date
- linked to the buyer's PayPal email
- personal and non-transferable
- valid for one Home Assistant installation
- verified locally using a signed offline license

---

## ✨ What makes Phoenix different

| | |
|---|---|
| 🧠 **AI Paper Trading** | Simulate a crypto portfolio and test ideas without risking real money |
| 🤖 **Automatic virtual positions** | Phoenix can open simulated paper positions from high-score setups |
| 📊 **Home Assistant dashboard** | Monitor equity, liquidity, open positions, profit/loss and mission progress |
| 📱 **Telegram alerts** | Receive alerts for virtual buys, market setups and profit/loss thresholds |
| 🎯 **Mission Mode** | Set an initial capital, target capital and time goal |
| 🏠 **Native entities** | Use sensors and binary sensors in dashboards, scripts and automations |
| 🔐 **24h trial + annual license** | Try Phoenix first, then unlock it with a personal signed annual license |
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
- 📱 Telegram diagnostics

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
- Home Assistant Telegram notify service, for example `notify.telegram`
- Optional Telegram Chat ID / target
- Profit / loss alert threshold in EUR
- Profit / loss alert threshold in percent
- Alert cooldown time

No manual YAML configuration is required for Phoenix itself.

> 📱 **Telegram requirement:** Phoenix does not create or configure the Telegram bot automatically. To receive Telegram alerts, you must first configure a working Telegram `notify` service in Home Assistant.

---

## 🧾 Changing License or Settings

Phoenix supports the Home Assistant **Configure** button and an in-panel Phoenix settings page.

Go to:

```text
Settings → Devices & services → Phoenix AI Trader → Configure
```

or open:

```text
Phoenix AI Trader → Settings Phoenix
```

From there you can update:

- license email
- activation code
- Telegram notifications
- Telegram notify service
- Telegram Chat ID / target
- alert thresholds
- mission settings

Private fields such as license key and Telegram Chat ID are preserved when left empty. To intentionally clear a saved private value, enter:

```text
CLEAR
```

---

## 📱 Telegram Notifications — Complete Setup

Phoenix can send Home Assistant `notify` alerts for:

- automatic paper buy events
- high-score market setups
- simulated profit/loss thresholds
- Phoenix startup/status checks

Phoenix **does not** create the Telegram bot and **does not** configure the Home Assistant Telegram integration automatically. Telegram must already work in Home Assistant before Phoenix can use it.

### 1. Configure Telegram in Home Assistant first

Before enabling Telegram in Phoenix, make sure that Home Assistant already has a working Telegram notification service.

Typical examples are:

```text
notify.telegram
notify.telegram_bot
notify.pasquale
notify.telegram_pasquale
```

The exact name depends on your Home Assistant configuration.

### 2. Test your notify service manually

In Home Assistant open:

```text
Developer Tools → Actions
```

Run a direct notify test such as:

```yaml
action: notify.telegram_pasquale
data:
  message: "Test Telegram from Home Assistant"
```

If this does not work, fix Telegram in Home Assistant before troubleshooting Phoenix.

### 3. Fill in Phoenix settings

Open:

```text
Phoenix AI Trader → Settings Phoenix
```

Then configure:

```text
Telegram enabled: Yes
Telegram service: notify.telegram_pasquale
Telegram Chat ID: optional
```

If your Home Assistant notify service already has a fixed recipient configured, leave the Chat ID field empty.

If you previously saved a wrong Chat ID, enter:

```text
CLEAR
```

then save settings.

### 4. Save and test

Click:

```text
Save settings
```

Then click:

```text
Test Telegram
```

Phoenix will send:

```text
Test Telegram Passato
```

### 5. MarkdownV2 compatibility

Since version **0.4.1**, Phoenix automatically escapes Telegram MarkdownV2 reserved characters before sending alerts. This prevents Telegram errors such as:

```text
Can't parse entities: character '.' is reserved and must be escaped
```

### 6. Troubleshooting

If the test fails:

1. Check that the Telegram bot works outside Phoenix.
2. Go to **Developer Tools → Actions** and manually test your `notify.telegram` service.
3. Verify that the service name entered in Phoenix is exactly correct.
4. If your service requires a target, enter the Telegram Chat ID in Phoenix.
5. If a wrong Chat ID is saved, enter `CLEAR`, save and test again.
6. Check Home Assistant logs for errors related to `phoenix`, `telegram` or `notify`.
7. Restart Home Assistant after updating Phoenix.

Useful log checks from Home Assistant terminal:

```bash
ha core logs -n 200 | grep -i phoenix
ha core logs -n 200 | grep -i telegram
```

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

### Updating

If HACS does not immediately detect a new commit:

1. Open **HACS → Integrations → Phoenix AI Trader**.
2. Use **Redownload** / **Download again**.
3. Restart Home Assistant.
4. Check the public status file:

```text
/local/phoenix-ai-trader-ha/status.json
```

The `version` field should match the current release.

---

## 📁 Default Data Folder

```text
/config/phoenix-ai-trader-ha
```

The integration automatically generates all required files inside this folder.

Public status mirrors are also written to:

```text
/config/www/phoenix-ai-trader-ha/status.json
/config/www/phoenix-ai-trader-ha/phoenix_status.json
```

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

## ⚠️ Financial Disclaimer and User Responsibility

Phoenix AI Trader is a **simulation, study and Paper Trading tool**. It is not a financial advisor, does not provide investment recommendations and does not guarantee any financial result.

All information, scores, Telegram alerts, simulations and data displayed by Phoenix are provided only for educational and informational purposes.

The author is not responsible for:

- real financial losses
- investment decisions made by the user
- improper use of the software
- incorrect interpretation of the data
- direct or indirect damages resulting from the use of Phoenix

The user is solely responsible for their own financial decisions. Any real market operation must be carried out responsibly, consciously and, when appropriate, with the support of a qualified professional.

Phoenix AI Trader **does not execute real trades**, **does not manage real funds** and **must not be used as a substitute for professional financial advice**.

---

## 💬 Support

| | |
|---|---|
| 🐛 **Bugs** | Open a GitHub Issue |
| 💡 **Ideas** | Use GitHub Discussions or contact the developer |
| 🔑 **License** | Annual license · Launch offer: **9.99 € for 15 days**, then **19.99 €/year** · PayPal purchase → signed license by email |
| 📱 **Telegram** | Requires an already configured Home Assistant Telegram `notify` service |
| 🇮🇹 **Italian support** | Italian documentation available in [README.it.md](README.it.md) |

---

## 📡 Planned Features

Upcoming releases may include:

- 📈 Real market data integration
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

A valid annual license grants personal, non-transferable use on the purchaser's own Home Assistant instance for 12 months from the issue date.

Redistribution, resale, sublicensing, publishing modified copies, or making the software available to third parties is not allowed without written permission.

---

<div align="center">

## 🦅 Phoenix AI Trader

**AI-powered Paper Trading for Home Assistant.**

Built with ❤️ by PakyITA.

</div>
