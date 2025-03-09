import os
from telethon import TelegramClient, events
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

ABH = TelegramClient("ubot", api_id, api_hash)

plugin_category = "extra"
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

async def delete_filtered_messages():
    chat_id = -1001968219024

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الروابط": InputMessagesFilterUrl,
            "الصور": InputMessagesFilterPhotos
        }

        total_deleted = 0
        deleted_counts = {key: 0 for key in filters.keys()}

        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                deleted_counts[msg_type] += 1
                total_deleted += 1

    except Exception as e:
        print(f"حدث خطأ أثناء الحذف: {str(e)}")

scheduler = AsyncIOScheduler()
scheduler.add_job(delete_filtered_messages, 'interval', hours=10)
scheduler.start()

ABH.start()
ABH.run_until_disconnected()
