from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import os

api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  

client = TelegramClient('session_name', api_id, api_hash)

bot_usernames = [
    "@VIPABH_BOT", "@werewolfbot", "@D7Bot",
    '@wueqbot', '@V2V1VBOT', '@ABHDAYSBOT',
    '@A_B_Hbot', '@Vipabhbot', '@Games_abhbot', 
    '@KiwetBOT', '@Hauehshbot', '@Ttoothbot',
    '@TT_TABOT', '@Hushsyhbot', '@Viphashbot',
    '@Httttghgttbot', '@Hshshjejeiiiiibot', '@Gagaggshbot',
    '@Ie_t2bot', '@k_4x1BOT', '@k_4x10bot', '@Hshjshdjbbot',
    '@Usuydhbbot', '@Udiehsjjdjdbbot', '@Usuwuwheuufbot',
    '@Audueysabot', '@Jajshshhdbot', '@Huqisijshnhbbbot',
    '@Hquwubsbbbot', '@Jajiuehehxjbbot', '@Shaysyshdhhdhbot',
    '@Bsbxxbdbabsbbot', '@Jajsjjbbbot', '@Jajajjbbbot',
    '@Jajajajjjbot', '@Abnhashbot'

    ]
@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_group(event):
    group_id = event.chat_id
    success_list = []
    failed_list = []
    
    try:
        chat = await client.get_entity(group_id)
        
        for bot_username in bot_usernames:
            try:
                bot = await client.get_entity(bot_username)
                
                if hasattr(chat, 'megagroup') and chat.megagroup:
                    await client(InviteToChannelRequest(group_id, [bot.id]))
                else:
                    await client(AddChatUserRequest(group_id, bot.id, fwd_limit=10))
                
                success_list.append(bot_username)
            except Exception as bot_error:
                failed_list.append(f"{bot_username} ({bot_error})")

        response = "✅ تمت إضافة البوتات بنجاح:\n" + "\n".join(success_list) if success_list else "❌ لم يتم إضافة أي بوت."
        if failed_list:
            response += "\n\n⚠️ فشل في إضافة بعض البوتات:\n" + "\n".join(failed_list)

        await event.reply(response)

    except Exception as e:
        await event.reply(f'❌ حدث خطأ أثناء محاولة إضافة البوتات: {e}')

with client:
    client.run_until_disconnected()
