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

delete_count = {
    "الملفات": 0,
    "الصور": 0,
    "الفيديوهات": 0,
    "المتحركات (GIF)": 0,
    "الملفات الصوتية": 0,
    "الرسائل الصوتية المرئية": 0,
    "الروابط": 0,
    "الملصقات": 0
}

async def delete_filtered_messages():
    chat_id = -1001968219024

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الصور": InputMessagesFilterPhotos,
            "الفيديوهات": InputMessagesFilterVideo,
            "المتحركات (GIF)": InputMessagesFilterGif,
            "الملفات الصوتية": InputMessagesFilterMusic,
            "الرسائل الصوتية المرئية": InputMessagesFilterRoundVideo,
            "الروابط": InputMessagesFilterUrl
        }

        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                delete_count[msg_type] += 1 
                print(f"تم حذف رسالة من النوع {msg_type}")

        async for message in ABH.iter_messages(chat_id):
            if message.sticker:
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                delete_count["الملصقات"] += 1
                print("تم حذف ملصق (Sticker)")

    except Exception as e:
        print(f"حدث خطأ أثناء الحذف: {str(e)}")

scheduler = AsyncIOScheduler()
scheduler.add_job(delete_filtered_messages, 'interval', minutes=5)

uid = [1910015590]

@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_on_command(event):
    id = event.sender_id
    if id in uid: 
        await delete_filtered_messages()
        
        report = "\n".join([f"{msg_type}: {count} رسالة" for msg_type, count in delete_count.items() if count > 0])
        await event.reply(f"تم الحذف بنجاح!\n\nتقرير الحذف:\n{report}")
    else:
        await event.reply("صديقي الامر خاص بالمشرفين , خلي ابن هاشم يضيفك بي ```ههههه```")
        return

async def main():
    await ABH.start()
    scheduler.start()
    await ABH.run_until_disconnected()

asyncio.run(main())
