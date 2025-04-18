import requests
from telegram import Bot
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
import os
# ----------------------- GYM FUNCTIONS -----------------------
def get_gym_capacity():
    url = "https://basic.deporweb.net/api/aforo/v1/actual/MA=="
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    return data["datos"]["AforoActual"]

# ----------------------- TELEGRAM FUNCTIONS -----------------------
def get_chat_id():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    data = response.json()
    return data["result"][0]["message"]["chat"]["id"]

# Function to send a Telegram message
async def send_telegram_notification(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# ----------------------- CONFIG -----------------------
# Gym API Endpoint
GYM_API_URL = "https://basic.deporweb.net/api/aforo/v1/actual/MA=="

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if not TELEGRAM_CHAT_ID:
    TELEGRAM_CHAT_ID = get_chat_id()

# ----------------------- MAIN FUNCTION -----------------------
if __name__ == "__main__":
    gym_capacity = get_gym_capacity()
    if gym_capacity <= 20:
        asyncio.run(send_telegram_notification(f"Aforo actual: {gym_capacity}%\nHora: {datetime.now(tz=ZoneInfo('Europe/Madrid')).strftime('%H:%M:%S')}"))
