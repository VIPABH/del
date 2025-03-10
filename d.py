import os, asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import (
    InputMessagesFilterDocument, InputMessagesFilterPhotos, InputMessagesFilterUrl,
    InputMessagesFilterVideo, InputMessagesFilterGif, InputMessagesFilterMusic,
    InputMessagesFilterRoundVideo
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

api_id, api_hash = os.getenv('API_ID'), os.getenv('API_HASH')
if not api_id or not api_hash:
    raise ValueError("API_ID و API_HASH يجب أن يكونا موجودين في البيئة")

ABH = TelegramClient("ubot", api_id, api_hash)
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

async def delete_filtered_messages():
    global delete_count
    delete_count = {"الملفات": 0, "الصور": 0, "الفيديوهات": 0, "المتحركات (GIF)": 0,
                    "الملفات الصوتية": 0, "الرسائل الصوتية المرئية": 0, "الروابط": 0, "الملصقات": 0}
    chat_id, cutoff_date = -1001968219024, datetime.utcnow() - timedelta(days=2)
    try:
        filters = {"الملفات": InputMessagesFilterDocument, "الصور": InputMessagesFilterPhotos,
                   "الفيديوهات": InputMessagesFilterVideo, "المتحركات (GIF)": InputMessagesFilterGif,
                   "الملفات الصوتية": InputMessagesFilterMusic, "الرسائل الصوتية المرئية": InputMessagesFilterRoundVideo,
                   "الروابط": InputMessagesFilterUrl}

        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter, limit=900):
                if message.date < cutoff_date or message.sender_id in excluded_user_ids:
                    break
                await message.delete()
                delete_count[msg_type] += 1

        async for message in ABH.iter_messages(chat_id, limit=900):
            if message.date < cutoff_date or message.sender_id in excluded_user_ids:
                break
            if message.sticker:
                await message.delete()
                delete_count["الملصقات"] += 1
    except Exception as e:
        print(f"خطأ أثناء الحذف: {e}")

scheduler = AsyncIOScheduler()
scheduler.add_job(delete_filtered_messages, 'interval', minutes=90)

uid = [1910015590, 890952036, 6359569537, 5914876113, 6498922948, 7615088480, 704233200,
       6164435743, 1122162341, 1260870186, 6783332896, 7722512961, 1494932118, 7483592520, 201728276, 7400171284]

@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_on_command(event):
    global delete_count
    if event.sender_id in uid:
        await event.respond('جاري الحذف انتظر...')
        await delete_filtered_messages()
        report = "\n".join([f"{msg_type}: {count} رسالة" for msg_type, count in delete_count.items() if count > 0])
        await event.respond(f"تم الحذف بنجاح!\n\nتقرير الحذف:\n{report}" if report else "لم يتم العثور على أي رسائل للحذف.")
    else:
        await event.reply("صديقي الامر خاص بالمشرفين , خلي ياسر يضيفك بي ```ههههه```")

async def main():
    await ABH.start()
    scheduler.start()
    await ABH.run_until_disconnected()

if __name__ == "__main__":
    ABH.loop.run_until_complete(main())
