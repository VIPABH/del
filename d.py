from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_group(event):
    message = event.message.text.split()

    if len(message) < 2:
        await event.reply('يجب أن تكتب اسم المجموعة بعد الأمر /add_bot')
        return

    # اسم البوت ثابت
    bot_username = "@VIPABH_BOT"  
    # الـ chat_id للمجموعة التي يتم إرسال الرسالة فيها
    group_id = event.chat_id

    try:
        # الحصول على معلومات البوت باستخدام الـ username
        bot = await client.get_entity(bot_username)

        # في حال كان البوت ID خاصًا، نقوم بتحديده مباشرةً
        bot_id = 7908156943  # ID الخاص بالبوت إذا لزم الأمر

        # التحقق من الـ chat_id
        chat = await client.get_entity(group_id)  # الحصول على الـ entity للمجموعة

        # إذا كانت المحادثة قناة ضخمة أو قناة، استخدم InviteToChannelRequest
        if hasattr(chat, 'megagroup') and chat.megagroup:
            await client(InviteToChannelRequest(channel=group_id, users=[bot_id]))  # إضافة البوت للقناة
            await event.reply(f'تمت دعوة البوت {bot_username} إلى القناة أو المجموعة بنجاح!')
        else:
            await client(AddChatUserRequest(chat_id=group_id, user_id=bot_id, fwd_limit=10))  # إضافة البوت للمجموعة العادية
            await event.reply(f'تمت إضافة البوت {bot_username} إلى المجموعة بنجاح!')
    except Exception as e:
        await event.reply(f'حدث خطأ أثناء إضافة البوت: {e}')

with client:
    client.run_until_disconnected()
