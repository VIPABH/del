from telethon import TelegramClient, events
from telethon.tl.functions.messages import AddChatUserRequest
import os 
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = "+964 770 598 4153"
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_group(event):
    # استخراج النص بعد الأمر
    message = event.message.text.strip()
    parts = message.split()

    # تحقق من وجود الأجزاء المطلوبة: الأمر واسم البوت
    if len(parts) < 2:
        await event.reply('يجب عليك كتابة اسم البوت بعد الأمر /add_bot.')
        return

    # استخراج اسم البوت من الرسالة
    bot_username = "@VIPABH_BOT"  # البوت الذي سيتم إضافته
    group_id = event.chat_id  # استخدام ID المجموعة التي تم فيها إرسال الرسالة

    try:
        # الحصول على معلومات البوت
        bot = await client.get_entity(bot_username)
        
        # إضافة البوت إلى المجموعة
        await client(AddChatUserRequest(
            chat_id=group_id,
            user_id=bot.id,
            fwd_limit=10  # عدد الرسائل التي يمكن إعادة توجيهها من البوت
        ))

        await event.reply(f'تمت إضافة البوت {bot_username} إلى المجموعة بنجاح!')
    except Exception as e:
        await event.reply(f'حدث خطأ أثناء إضافة البوت: {e}')

with client:
    client.run_until_disconnected()
