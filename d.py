import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# تأكد من أن بيانات البيئة موجودة
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

if not api_id or not api_hash:
    raise ValueError("API_ID و API_HASH يجب أن يكونا موجودين في البيئة")

ABH = TelegramClient("ubot", api_id, api_hash)

plugin_category = "extra"
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

# الدالة لحذف الرسائل
async def delete_filtered_messages():
    chat_id = -1001996913931  # معرف القناة

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الروابط": InputMessagesFilterUrl,
            "الصور": InputMessagesFilterPhotos
        }

        # مسح جميع الأنواع في كل دورة
        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                print(f"تم حذف رسالة من النوع {msg_type}")  # سجل الحذف

    except Exception as e:
        print(f"حدث خطأ أثناء الحذف: {str(e)}")

# جدولة الحذف كل 5 دقائق
scheduler = AsyncIOScheduler()
scheduler.add_job(delete_filtered_messages, 'interval', minutes=5)

# الحدث لتنفيذ الحذف عند إرسال الأمر "امسح"
@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_on_command(event):
    if event.sender_id != 1910015590:  # تحقق من أن المرسل هو الذي يملك الحق في الحذف
        return

    await delete_filtered_messages()
    await event.reply("تم الحذف بنجاح!")

# الدالة الرئيسية لتشغيل البوت
async def main():
    await ABH.start()
    scheduler.start()  # بدء الجدولة
    await ABH.run_until_disconnected()

# تشغيل البوت
asyncio.run(main())
