import os
import time
import requests
from dotenv import load_dotenv

# =====================
# Load ENV
# =====================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ BOT_TOKEN یا OPENAI_API_KEY ست نشده")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# =====================
# User State
# =====================
users = {}

# =====================
# Telegram Helpers
# =====================
def get_updates(offset=None):
    try:
        params = {"timeout": 60}
        if offset:
            params["offset"] = offset
        r = requests.get(
            f"{BASE_URL}/getUpdates",
            params=params,
            timeout=(10, 70)
        )
        return r.json()
    except Exception as e:
        print("❌ getUpdates error:", e)
        return {"ok": False}

def send_message(chat_id, text, reply_markup=None):
    try:
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        if reply_markup:
            payload["reply_markup"] = reply_markup

        requests.post(
            f"{BASE_URL}/sendMessage",
            json=payload,
            timeout=15
        )
    except Exception as e:
        print("❌ sendMessage error:", e)

# =====================
# OpenAI Caption
# =====================
def generate_caption(plan, topic, details):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = {
        "basic": "یک کپشن ساده و کوتاه اینستاگرامی برای سالن زیبایی بنویس.",
        "pro": "یک کپشن حرفه‌ای اینستاگرامی با CTA و هشتگ بنویس.",
        "vip": "یک کپشن بسیار حرفه‌ای، احساسی، فروش‌محور با هشتگ هدفمند بنویس."
    }[plan]

    prompt = f"""
موضوع: {topic}
جزئیات: {details}
"""

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }

    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ OpenAI error:", e)
        return "❌ خطا در تولید کپشن"

# =====================
# Bot Logic
# =====================
def handle_start(chat_id):
    users[chat_id] = {
        "state": "CHOOSE_PLAN",
        "plan": None,
        "topic": None
    }

    text = (
        "🤖 ربات تولید کپشن اینستاگرام مخصوص سالن‌های زیبایی\n\n"
        "🎁 می‌تونی پلن‌ها رو تست کنی و تفاوت خروجی رو ببینی\n"
        "👇 یکی رو انتخاب کن:"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🟦 پلن پایه", "callback_data": "plan_basic"}],
            [{"text": "🟪 پلن حرفه‌ای", "callback_data": "plan_pro"}],
            [{"text": "🟨 پلن VIP", "callback_data": "plan_vip"}]
        ]
    }

    send_message(chat_id, text, keyboard)

def handle_callback(chat_id, data):
    if chat_id not in users:
        return

    if data.startswith("plan_"):
        plan = data.replace("plan_", "")
        users[chat_id]["plan"] = plan
        users[chat_id]["state"] = "GET_TOPIC"

        send_message(
            chat_id,
            "✍️ موضوع پست چیه؟\nمثلاً: کاشت ناخن، رنگ مو، فیشیال"
        )

def handle_text(chat_id, text):
    if chat_id not in users:
        handle_start(chat_id)
        return

    state = users[chat_id]["state"]

    if state == "GET_TOPIC":
        users[chat_id]["topic"] = text
        users[chat_id]["state"] = "GET_DETAILS"

        send_message(
            chat_id,
            "📝 یک توضیح کوتاه بده:\nمثلاً نوع خدمات، حس پست، مخاطب هدف"
        )

    elif state == "GET_DETAILS":
        plan = users[chat_id]["plan"]
        topic = users[chat_id]["topic"]

        caption = generate_caption(plan, topic, text)

        send_message(
            chat_id,
            f"✨ کپشن پیشنهادی ({plan.upper()}):\n\n{caption}"
        )

        users[chat_id]["state"] = "CHOOSE_PLAN"

# =====================
# Main Loop
# =====================
def main():
    offset = None
    print("🤖 Bot is running...")

    while True:
        updates = get_updates(offset)
        if updates.get("ok"):
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")

                    if text.lower() == "/start":
                        handle_start(chat_id)
                    else:
                        handle_text(chat_id, text)

                elif "callback_query" in update:
                    cb = update["callback_query"]
                    chat_id = cb["message"]["chat"]["id"]
                    handle_callback(chat_id, cb["data"])

        time.sleep(1)

if __name__ == "__main__":
    main()
