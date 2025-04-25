# 🤖 Post Forwarder Telegram Bot

A simple Telegram bot that listens to messages sent to it and **forwards those messages to one or more Telegram channels** automatically.

No fancy libraries, pure Python using `requests` and Telegram Bot API.

---

## ✨ Features

- Forward any type of message (text, media, files)
- Forward to **multiple channels** at once
- Admin-only access
- Runs on free hosting like **Render**

---

## 📦 Environment Variables

You need to set the following environment variables:

| Variable Name  | Description                            |
|----------------|----------------------------------------|
| `BOT_TOKEN`    | Your Telegram bot token from BotFather |
| `CHANNEL_IDS`  | Comma-separated channel IDs to forward to (with `-100`) |
| `OWNER_ID`     | Your numeric Telegram user ID          |

📝 Example:
```
CHANNEL_IDS=-1001234567890,-1009876543210
```

---

## 🚀 Deployment (Render)

### ✅ Requirements:
- Python 3.10+
- `requests` & `flask` packages

## 🔐 Owner-Only Logic
Only the user with `OWNER_ID` can interact with the bot.

---

## 🧠 How It Works
- Bot uses `getUpdates` (long polling)
- When it receives a message from owner, it forwards it to all `CHANNEL_IDS`

---

## 🙌 Credits
Made by [@priyanshusingh999](https://github.com/priyanshusingh999)

Want to customize or upgrade this bot? Feel free to fork!

