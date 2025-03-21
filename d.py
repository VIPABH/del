from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import os

api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  

client = TelegramClient('session_name', api_id, api_hash)

# قائمة البوتات المراد إضافتها
bot_usernames = ["@VIPABH_BOT", "@werewolfbot ", "@D7Bot "]  
bot_ids = [7908156943, 1234567890, 987654321]  # معرفات البوتات

@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_group(event):
    group_id = event.chat_id
    try:
        chat = await client.get_entity(group_id)
        for bot_username, bot_id in zip(bot_usernames, bot_ids):
            bot = await client.get_entity(bot_username)
            
            if hasattr(chat, 'megagroup') and chat.megagroup:
                await client(InviteToChannelRequest(group_id, [bot_id]))
            else:
                await client(AddChatUserRequest(group_id, bot_id, fwd_limit=10))

            await event.reply(f'تمت إضافة البوت {bot_username} إلى المجموعة بنجاح!')
    
    except Exception as e:
        await event.reply(f'حدث خطأ أثناء إضافة البوت: {e}')

with client:
    client.run_until_disconnected()
