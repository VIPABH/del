from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import os

api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  

client = TelegramClient('session_name', api_id, api_hash)

# قائمة معرفات البوتات
bot_ids = [7908156943, 175844556, 1421907917]  

@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_group(event):
    group_id = event.chat_id
    success_list = []
    failed_list = []
    
    try:
        chat = await client.get_entity(group_id)
        
        for bot_id in bot_ids:
            try:
                if hasattr(chat, 'megagroup') and chat.megagroup:
                    await client(InviteToChannelRequest(group_id, [bot_id]))
                else:
                    await client(AddChatUserRequest(group_id, bot_id, fwd_limit=10))
                
                success_list.append(str(bot_id))  # تحويل الـ ID إلى نص للإبلاغ عنه
            except Exception as bot_error:
                failed_list.append(f"{bot_id} ({bot_error})")

        # إرسال تقرير بالنتيجة النهائية
        response = "✅ تمت إضافة البوتات بنجاح:\n" + "\n".join(success_list) if success_list else "❌ لم يتم إضافة أي بوت."
        if failed_list:
            response += "\n\n⚠️ فشل في إضافة بعض البوتات:\n" + "\n".join(failed_list)

        await event.reply(response)

    except Exception as e:
        await event.reply(f'❌ حدث خطأ أثناء محاولة إضافة البوتات: {e}')

with client:
    client.run_until_disconnected()
