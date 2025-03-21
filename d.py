from telethon import TelegramClient, events
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
import os 

API_ID = os.getenv('API_ID')  # تأكد من تعيين API_ID في البيئة الخاصة بك
API_HASH = os.getenv('API_HASH')  # تأكد من تعيين API_HASH في البيئة الخاصة بك
PHONE_NUMBER = "+964 770 598 4153"  # رقم هاتفك

client = TelegramClient('session_name', API_ID, API_HASH)

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
    bot_username = parts[1]  # سيتم أخذ اسم البوت من الرسالة
    group_id = event.chat_id  # استخدام ID المجموعة التي تم فيها إرسال الرسالة

    try:
        # الحصول على معلومات البوت
        bot = await client.get_entity(bot_username)
        
        # الحصول على معلومات المحادثة (المجموعة أو القناة)
        chat = await client.get_entity(group_id)

        # إذا كانت المحادثة من نوع قناة أو مجموعة ضخمة (MegaGroup)، نستخدم InviteToChannelRequest
        if hasattr(chat, 'megagroup') and (chat.megagroup or chat.broadcast):  # إذا كانت قناة أو مجموعة ضخمة (MegaGroup)
            await client(InviteToChannelRequest(
                channel=group_id,
                users=[bot.id]  # إضافة البوت إلى القناة أو المجموعة
            ))
            await event.reply(f'تمت دعوة البوت {bot_username} إلى القناة أو المجموعة بنجاح!')
        else:
            # إذا كانت محادثة عادية (Group)، نستخدم AddChatUserRequest
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
