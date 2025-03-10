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

excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

# الفلاتر المستخدمة
filters = {
    "الملفات": InputMessagesFilterDocument,
    "الصور": InputMessagesFilterPhotos,
    "الفيديوهات": InputMessagesFilterVideo,
    "المتحركات (GIF)": InputMessagesFilterGif,
    "الملفات الصوتية": InputMessagesFilterMusic,
    "الرسائل الصوتية المرئية": InputMessagesFilterRoundVideo,
    "الروابط": InputMessagesFilterUrl
}

# دالة الحذف
async def delete_filtered_messages(chat_id):
    try:
        total_deleted = 0
        deleted_counts = {key: 0 for key in filters.keys()}

        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue  
                if message:
                    await message.delete()
                    deleted_counts[msg_type] += 1
                    total_deleted += 1

        if total_deleted > 0:
            details = "\n".join([f"{msg_type}: {count}" for msg_type, count in deleted_counts.items() if count > 0])
            await ABH.send_message(chat_id, f"تم حذف {total_deleted} رسالة.\nالتفاصيل:\n{details}")
        else:
            await ABH.send_message(chat_id, "لا توجد رسائل تطابق الفلاتر المحددة!")

    except Exception as e:
        await ABH.send_message(chat_id, f"حدث خطأ أثناء الحذف: {str(e)}")

# تشغيل الحذف بالأمر "امسح"
@ABH.on(events.NewMessage(pattern="امسح$"))
async def manual_delete(event):
    await event.delete()
    await delete_filtered_messages(event.chat_id)

# تشغيل الحذف تلقائيًا كل ساعتين
scheduler = AsyncIOScheduler()

try:
    scheduler.add_job(delete_filtered_messages, "interval", hours=2, args=[-1001968219024])
    scheduler.start()
    print("✅ تمت جدولة عملية الحذف التلقائي كل ساعتين بنجاح!")
except Exception as e:
    print(f"⚠️ خطأ في جدولة الحذف التلقائي: {e}")

# تشغيل البوت
with ABH:
    ABH.run_until_disconnected()
