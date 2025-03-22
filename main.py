from telethon import TelegramClient
import os

# الحصول على المتغيرات من البيئة (يمكنك وضعها في ملف .env)
api_id = os.getenv('API_ID')      # احصل على API_ID من موقع Telegram API
api_hash = os.getenv('API_HASH')  # احصل على API_HASH من موقع Telegram API
bot_token = os.getenv('BOT_TOKEN')  # توكن البوت

# إنشاء client باستخدام TelegramClient
client = TelegramClient('bot_session', api_id, api_hash)

# بدء الاتصال باستخدام التوكن للبوت
async def start_bot():
    await client.start(bot_token=bot_token)
    print("Bot started successfully!")
