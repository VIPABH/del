import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterVoice,
    InputMessagesFilterRoundVideo
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

if not api_id or not api_hash:
    raise ValueError("API_ID و API_HASH يجب أن يكونا موجودين في البيئة")

ABH = TelegramClient("ubot", api_id, api_hash)

plugin_category = "extra"
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

async def delete_filtered_messages():
    chat_id = -1001996913931

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الصور": InputMessagesFilterPhotos,
            "الفيديوهات": InputMessagesFilterVideo,
            "المتحركات (GIF)": InputMessagesFilterGif,
            "الملفات الصوتية": InputMessagesFilterMusic,
            "الرسائل الصوتية": InputMessagesFilterVoice,
            "الرسائل الصوتية المرئية": InputMessagesFilterRoundVideo,
            "الروابط": InputMessagesFilterUrl
        }

        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                print(f"تم حذف رسالة من النوع {msg_type}")

        async for message in ABH.iter_messages(chat_id):  # حذف الملصقات يدويًا
            if message.sticker:
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                print("تم حذف ملصق (Sticker)")

    except Exception as e:
        print(f"حدث خطأ أثناء الحذف: {str(e)}")

scheduler = AsyncIOScheduler()
scheduler.add_job(delete_filtered_messages, 'interval', minutes=5)

@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_on_command(event):
    if event.sender_id != 1910015590:
        return

    await delete_filtered_messages()
    await event.reply("تم الحذف بنجاح!")

async def main():
    await ABH.start()
    scheduler.start()
    await ABH.run_until_disconnected()

asyncio.run(main())
