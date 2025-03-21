from telethon import TelegramClient, events
from telethon.tl.functions.messages import AddChatUserRequest
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_group(event):
    # الحصول على اسم البوت وID المجموعة من الرسالة
    message = event.message.text.split()
    
    if len(message) < 3:
        await event.reply('يجب أن تكتب اسم البوت وID المجموعة بعد الأمر /add_bot')
        return
    
    bot_username = message[1]  # أول كلمة بعد الأمر هي اسم البوت
    group_id = message[2]  # ثاني كلمة بعد الأمر هي ID المجموعة

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
