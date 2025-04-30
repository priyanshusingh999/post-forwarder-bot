import requests
import json
import time
import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '🤖 Bot is Running! Created By @devx_coder("priyanshusingh999")'

def run_flask():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()

# Config Variables from environment or fallback
#TOKEN = os.getenv('TOKEN') or ""
#OWNER_ID = int(os.getenv('OWNER_ID') or )
#FORCE_SUB_CHANNEL = os.getenv('FORCE_SUB_CHANNEL') or ""

API = f"https://api.telegram.org/bot{TOKEN}"
DB_FILE = "db.json"

# Database Functions
def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Telegram API Helpers
def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    requests.post(f"{API}/sendMessage", json=payload)

def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    response = requests.get(f"{API}/getUpdates", params=params).json()
    return response.get("result", [])

def get_member_status(user_id, channel_id):
    try:
        url = f"{API}/getChatMember"
        params = {"chat_id": channel_id, "user_id": user_id}
        r = requests.get(url, params=params).json()
        return r.get("result", {}).get("status", "left")
    except:
        return "left"

def copy_message(to_chat_id, message):
    try:
        if "text" in message:
            send_message(to_chat_id, message["text"])
        elif "photo" in message:
            photo = message["photo"][-1]["file_id"]
            caption = message.get("caption", "")
            requests.post(f"{API}/sendPhoto", json={
                "chat_id": to_chat_id,
                "photo": photo,
                "caption": caption
            })
        elif "video" in message:
            video = message["video"]["file_id"]
            caption = message.get("caption", "")
            requests.post(f"{API}/sendVideo", json={
                "chat_id": to_chat_id,
                "video": video,
                "caption": caption
            })
        elif "document" in message:
            doc = message["document"]["file_id"]
            caption = message.get("caption", "")
            requests.post(f"{API}/sendDocument", json={
                "chat_id": to_chat_id,
                "document": doc,
                "caption": caption
            })
        else:
            send_message(to_chat_id, "⚠️ Unsupported message type.")
    except Exception as e:
        print(f"Error copying message to {to_chat_id}: {e}")

def force_subscribe_message(chat_id):
    join_button = {
        "inline_keyboard": [[
            {
                "text": "🔗 Join Channel",
                "url": f"https://t.me/{FORCE_SUB_CHANNEL.strip('@')}"
            }
        ]]
    }
    send_message(
        chat_id,
        "🔒 Pehle hamare channel ko join karo tabhi aap bot ka use kar sakte ho.",
        reply_markup=json.dumps(join_button)
    )

# Bot Logic
def main():
    print("🤖 Bot is running...")
    db = load_db()
    offset = None

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            message = update.get("message")
            if not message:
                continue

            user_id = message["from"]["id"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            # Force Subscribe Check
            if FORCE_SUB_CHANNEL:
                status = get_member_status(user_id, FORCE_SUB_CHANNEL)
                if status in ["left", "kicked"]:
                    force_subscribe_message(chat_id)
                    continue

            # Initialize user data
            if str(user_id) not in db:
                db[str(user_id)] = {"channels": []}
                save_db(db)

            user_data = db[str(user_id)]
            user_channels = user_data.get("channels", [])

            # Command Handlers
            if text.startswith("/start"):
                send_message(chat_id, "👋 Welcome! Send any post and I’ll share it to your channels.")

            elif text.startswith("/addchannel"):
                try:
                    channel_ids = text.split(" ", 1)[1].split()
                    added = []
                    for cid in channel_ids:
                        if cid not in user_channels:
                            user_channels.append(cid)
                            added.append(cid)
                    save_db(db)
                    if added:
                        send_message(chat_id, f"✅ Added channel(s):\n" + "\n".join(added))
                    else:
                        send_message(chat_id, "ℹ️ All channels already added.")
                except:
                    send_message(chat_id, "❌ Usage: /addchannel <channel_id_1> <channel_id_2> ...")

            elif text.startswith("/removechannel"):
                try:
                    channel_ids = text.split(" ", 1)[1].split()
                    removed = []
                    for cid in channel_ids:
                        if cid in user_channels:
                            user_channels.remove(cid)
                            removed.append(cid)
                    save_db(db)
                    if removed:
                        send_message(chat_id, f"🗑️ Removed channel(s):\n" + "\n".join(removed))
                    else:
                        send_message(chat_id, "ℹ️ No matching channels found to remove.")
                except:
                    send_message(chat_id, "❌ Usage: /removechannel <channel_id_1> <channel_id_2> ...")

            elif text.startswith("/mychannels"):
                if not user_channels:
                    send_message(chat_id, "ℹ️ Aapne abhi tak koi channel add nahi kiya hai.")
                else:
                    send_message(chat_id, "📋 Aapke added channels:\n" + "\n".join(user_channels))

            elif text.startswith("/users") and user_id == OWNER_ID:
                send_message(chat_id, f"👥 Total users who used the bot: {len(db)}")

            elif text.startswith("/broadcast") and user_id == OWNER_ID:
                parts = text.split(" ", 1)
                if len(parts) < 2:
                    send_message(chat_id, "❌ Usage: /broadcast <your message>")
                    continue
                msg = parts[1]
                success, fail = 0, 0
                for uid in db:
                    try:
                        send_message(uid, f"📢 Broadcast from Admin:\n\n{msg}")
                        success += 1
                    except Exception as e:
                        fail += 1
                        print(f"❌ Failed to send to {uid}: {e}")
                send_message(chat_id, f"✅ Broadcast done.\n🟢 Sent: {success}\n🔴 Failed: {fail}")

            else:
                if not user_channels:
                    send_message(chat_id, "⚠️ Pehle /addchannel se channel add karo.")
                    continue
                for cid in user_channels:
                    try:
                        copy_message(cid, message)
                    except:
                        send_message(chat_id, f"❌ Couldn't post to {cid}")

        time.sleep(1)

# Run bot
if __name__ == "__main__":
    main()

