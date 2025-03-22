from telethon import TelegramClient
import os
from .config.abh import start_bot

# الحصول على المتغيرات من البيئة (يمكنك وضعها في ملف .env)
api_id = os.getenv('API_ID')      # احصل على API_ID من موقع Telegram API
api_hash = os.getenv('API_HASH')  # احصل على API_HASH من موقع Telegram API
bot_token = os.getenv('BOT_TOKEN')  # توكن البوت

# إنشاء client باستخدام TelegramClient
abh = TelegramClient('bot_session', api_id, api_hash)

import asyncio
asyncio.run(start_bot())

# بدء الاتصال باستخدام التوكن للبوت
async def start_bot():
    ABH.run_until_disconnected()
print("Bot started successfully!")
