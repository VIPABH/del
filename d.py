from telethon import TelegramClient, events
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterPhotos
from telethon.tl.functions.channels import GetParticipants
import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')

if not api_id or not api_hash:
    raise ValueError("API_ID و API_HASH يجب أن يكونا موجودين في البيئة")

ABH = TelegramClient("ubot", api_id, api_hash)

plugin_category = "extra"
excluded_user_ids = [793977288, 1421907917, 7308514832, 6387632922, 7908156943]

async def delete_filtered_messages():
    chat_id = -1001968219024

    try:
        filters = {
            "الملفات": InputMessagesFilterDocument,
            "الصور": InputMessagesFilterPhotos
        }

        for msg_type, msg_filter in filters.items():
            async for message in ABH.iter_messages(chat_id, filter=msg_filter):
                if message.sender_id in excluded_user_ids:
                    continue
                await message.delete()
                print(f"تم حذف رسالة من النوع {msg_type}")

    except Exception as e:
        print(f"حدث خطأ أثناء الحذف: {str(e)}")

async def is_admin(user_id, chat_id):
    try:
        # استدعاء GetParticipants للحصول على جميع المشاركين
        participants = await ABH(GetParticipants(channel=chat_id, filter='admins'))
        
        # تحقق إذا كان المستخدم مشرفًا
        for participant in participants.users:
            if participant.id == user_id:
                return True
        return False
    except Exception as e:
        print(f"خطأ أثناء التحقق من المشرفين: {str(e)}")
        return False

scheduler = AsyncIOScheduler()
scheduler.add_job(delete_filtered_messages, 'interval', minutes=60)

@ABH.on(events.NewMessage(pattern="امسح$"))
async def delete_on_command(event):
    if await is_admin(event.sender_id, event.chat_id):  # تحقق إذا كان المرسل مشرفًا
        await delete_filtered_messages()
        await event.reply("تم الحذف بنجاح!")
    else:
        await event.reply("أنت لست مشرفًا، لا يمكنك تنفيذ هذا الأمر.")

async def main():
    await ABH.start()
    scheduler.start()
    await ABH.run_until_disconnected()

asyncio.run(main())
