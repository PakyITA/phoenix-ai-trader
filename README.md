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
**📜 Changelog:** [CHANGELOG.md](CHANGELOG.md) · [Italian changelog](CHANGELOG.it.md)

---

**Phoenix AI Trader** brings a premium **Paper Trading experience** directly into **Home Assistant**.

Create a virtual crypto portfolio, monitor profit and loss, receive Telegram alerts and follow a personal capital mission — all without connecting to an exchange or risking real money.

> ⚠️ **Phoenix AI Trader is designed exclusively for Paper Trading.**
>
> It never connects to Binance, Bybit, Coinbase or any other exchange and never places real orders.

</div>

---

## 🆕 What's new in 0.4.1

Version **0.4.1** focuses on Telegram reliability and documentation cleanup.

- Fixed Telegram alerts blocked by Telegram MarkdownV2 parsing.
- Automatically escapes Telegram MarkdownV2 reserved characters before sending Phoenix alerts.
- Uses blocking Home Assistant service calls for Telegram alerts, so errors are easier to diagnose.
- Aligns the public `status.json` version with the internal integration version.
- Adds a dedicated Italian changelog.
- Keeps documentation generic by using examples such as `notify.telegram_user` and `notify.user`.
- Standardizes documentation files to `README.md` and `README.it.md`.

See [CHANGELOG.md](CHANGELOG.md) for details.

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

After payment, the signed license is sent by email.

---

## ✨ What makes Phoenix different

| | |
|---|---|
| 🧠 **AI Paper Trading** | Simulate a crypto portfolio and test ideas without risking real money |
| 📊 **Home Assistant dashboard** | Monitor equity, liquidity, open positions, profit/loss and mission progress |
| 📱 **Telegram alerts** | Receive alerts for automatic paper trades, high-score setups and profit/loss thresholds |
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
- Home Assistant Telegram notify service, for example `notify.telegram_user`
- Optional Telegram Chat ID / target
- Profit / loss alert threshold in EUR
- Profit / loss alert threshold in percent
- Alert cooldown time

No manual YAML configuration is required for Phoenix itself.

> 📱 **Telegram requirement:** Phoenix does not create or configure the Telegram bot automatically. To receive Telegram alerts, you must first configure a working Telegram `notify` service in Home Assistant, then enter the service name and, when required by your Home Assistant setup, the Telegram Chat ID in Phoenix.

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

Private values such as activation code and Telegram Chat ID are preserved when their fields are left empty. To clear a saved private value, enter:

```text
CLEAR
```

---

## 📱 Telegram Notifications — Complete Setup

Phoenix can send Home Assistant `notify` alerts for automatic paper trades, high-score market setups and profit/loss thresholds.

Phoenix does **not** create the Telegram bot and does **not** configure the Home Assistant Telegram integration automatically. Telegram must already work in Home Assistant before Phoenix can use it.

### 1. Configure Telegram in Home Assistant first

Before enabling Telegram in Phoenix, make sure that Home Assistant already has a working Telegram notification service.

Typical examples are:

```text
notify.telegram
notify.telegram_user
notify.user
```

The exact name depends on your Home Assistant configuration.

### 2. Find the correct notify service name

In Home Assistant open:

```text
Developer Tools → Services
```

Search for:

```text
notify.
```

Then identify the Telegram service you normally use to send messages.

Phoenix must receive the full service name, including `notify.`.

Example:

```text
notify.telegram_user
```

### 3. Telegram Chat ID

Some Home Assistant Telegram configurations already include a default target. In that case, Phoenix can send messages using only `message`.

Other configurations require a target. In that case, Phoenix also needs the Telegram **Chat ID**.

The Chat ID can be:

```text
123456789
```

or, for groups/channels, it can look like:

```text
-1001234567890
```

If your Home Assistant notify service already has a fixed recipient configured, leave the Chat ID field empty.

### 4. Fill in Phoenix settings

Open:

```text
Phoenix AI Trader → Settings Phoenix
```

Then configure:

```text
Telegram enabled: Yes
Telegram service: notify.telegram_user
Telegram Chat ID: optional
```

### 5. Save and test

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

If the Chat ID field is empty, Phoenix sends only:

```yaml
message: "Test Telegram Passato"
```

If the Chat ID field is filled, Phoenix can send the message with an explicit target.

### 6. Troubleshooting

If the test fails:

1. Check that the Telegram bot works outside Phoenix.
2. Go to **Developer Tools → Services** and manually test your notify service.
3. Verify that the service name entered in Phoenix is exactly correct.
4. If your service requires a target, enter the Telegram Chat ID in Phoenix.
5. Check Home Assistant logs for errors related to `phoenix`, `telegram` or `notify`.
6. Restart Home Assistant after updating Phoenix.

Useful log checks from Home Assistant terminal:

```bash
ha core logs -n 200 | grep -i phoenix
ha core logs -n 200 | grep -i telegram
```

### MarkdownV2 note

Home Assistant Telegram setups may use MarkdownV2 parsing. Phoenix 0.4.1 automatically escapes reserved MarkdownV2 characters before sending alerts, preventing errors such as:

```text
Can't parse entities: character '.' is reserved and must be escaped
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

### Updating Phoenix

If HACS does not immediately show the update, open Phoenix in HACS and use:

```text
Redownload / Scarica di nuovo
```

Then restart Home Assistant.

After updating, the public status file should report:

```json
"version": "0.4.1"
```

Public status URL example:

```text
http://HOME_ASSISTANT_IP:8123/local/phoenix-ai-trader-ha/status.json
```

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
| 📱 **Telegram** | Requires an already configured Home Assistant Telegram `notify` service and may require a Telegram Chat ID / target |
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

A valid annual license grants personal, non-transferable use on the purchaser's own Home Assistant instance for 12 months from the issue date.

Redistribution, resale, sublicensing, publishing modified copies, or making the software available to third parties is not allowed without written permission.

---

<div align="center">

## 🦅 Phoenix AI Trader

**AI-powered Paper Trading for Home Assistant.**

Built with ❤️ by PakyITA.

</div>
