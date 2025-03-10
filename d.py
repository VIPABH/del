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

# تحميل API_ID و API_HASH من البيئة
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

# التحقق من وجود API_ID و API_HASH
if not api_id or not api_hash:
    raise ValueError("API_ID و API_HASH يجب أن يكونا موجودين في البيئة")

# إنشاء العميل
ABH = TelegramClient("ubot", api_id, api_hash)

# قائمة المستخدمين المستبعدين
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_filtered_messages(event):
    # حذف الرسالة التي تحتوي على الأمر "امسح"
    await event.delete()
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

        total_deleted = 0 
        deleted_counts = {key: 0 for key in filters.keys()}

        # تكرار جميع الرسائل مع الفلاتر المحددة
        for msg_type, msg_filter in filters.items():
            async for message in event.client.iter_messages(event.chat_id, filter=msg_filter):
                # تخطي الرسائل من المستخدمين المستبعدين
                if message.sender_id in excluded_user_ids:
                    continue 
                if message:
                    await message.delete()
                    deleted_counts[msg_type] += 1
                    total_deleted += 1

        # إذا تم حذف رسائل، إظهار تفاصيل الحذف
        if total_deleted > 0:
            details = "\n".join([f"{msg_type}: {count}" for msg_type, count in deleted_counts.items() if count > 0])
            await event.reply(f"تم حذف {total_deleted} رسالة.\nالتفاصيل:\n{details}")
        else:
            await event.reply("لا توجد رسائل تطابق الفلاتر المحددة!")

    except Exception as e:
        await event.reply(f"حدث خطأ أثناء الحذف: {str(e)}")

# طباعة رسالة تفيد بأن البوت يعمل
print('del is working ✓')

# تشغيل العميل
ABH.run_until_disconnected()
