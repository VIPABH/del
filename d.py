import os
from telethon import *
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterPhotos,
    InputMessagesFilterUrl
)

# api_id = os.getenv('API_ID')      
# api_hash = os.getenv('API_HASH')

api_id = 28576958
api_hash = '7b1613615205f3ebfe774b54c3a47358'

ABH = TelegramClient("ubot", api_id, api_hash)

plugin_category = "extra"

excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_filtered_messages(event):
    if event.sender_id != 1910015590:
        return

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الروابط": InputMessagesFilterUrl,
            "الصور": InputMessagesFilterPhotos
        }

        total_deleted = 0 
        deleted_counts = {key: 0 for key in filters.keys()}


        for msg_type, msg_filter in filters.items():
            async for message in event.client.iter_messages(event.chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue 
                if message:
                    await message.delete()
                    deleted_counts[msg_type] += 1
                    total_deleted += 1

        if total_deleted > 0:
            details = "\n".join([f"{msg_type}: {count}" for msg_type, count in deleted_counts.items() if count > 0])
            await event.reply(f"تم حذف {total_deleted} رسالة.\nالتفاصيل:\n{details}")
        else:
            await event.reply("لا توجد رسائل تطابق الفلاتر المحددة!")

    except Exception as e:
        # التعامل مع الأخطاء
        await event.reply(f"حدث خطأ أثناء الحذف: {str(e)}")

ABH.start()
ABH.run_until_disconnected()
