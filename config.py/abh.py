from telethon import TelegramClient
import os
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('code', api_id, api_hash)
async def start_bot():
    await ABH.start(bot_token=bot_token)
    print("✅ Telegram bot is running!")
