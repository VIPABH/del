import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
import os

api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  

client = TelegramClient('session_name', api_id, api_hash)

bot_usernames = [
    "@VIPABH_BOT", '@A_B_Hbot', '@Vipabhbot', '@Games_abhbot', 
    '@Hquwubsbbbot', '@Jajiuehehxjbbot', '@Shaysyshdhhdhbot',
    '@Ie_t2bot', '@k_4x1BOT', '@k_4x10bot', '@Hshjshdjbbot',
    '@Httttghgttbot', '@Hshshjejeiiiiibot', '@Gagaggshbot',
    '@Audueysabot', '@Jajshshhdbot', '@Huqisijshnhbbbot',
    '@Usuydhbbot', '@Udiehsjjdjdbbot', '@Usuwuwheuufbot',
    '@Bsbxxbdbabsbbbot', '@Jajsjjbbbot', '@Jajajjbbbot',
    '@TT_TABOT', '@Hushsyhbot', '@Viphashbot',
    '@KiwetBOT', '@Hauehshbot', '@Ttoothbot',
    '@Jajajajjjbot', '@Abnhashbot'
]

@client.on(events.NewMessage(pattern='/add_bot'))
async def add_bot_to_chat(event):
    chat_id = event.chat_id
    success_list = []
    failed_list = []

    try:
        chat = await client.get_entity(chat_id)
        is_channel = event.is_channel  # معرفة ما إذا كان الهدف قناة أم مجموعة

        for bot_username in bot_usernames:
            try:
                bot = await client.get_entity(bot_username)

                if is_channel:
                    await client(InviteToChannelRequest(chat_id, [bot.id]))
                else:
                    await client(AddChatUserRequest(chat_id, bot.id, fwd_limit=10))
                
                success_list.append(bot_username)
                await asyncio.sleep(5)  # تأخير 5 ثواني بين كل محاولة لتجنب الحظر
                
            except Exception as bot_error:
                if "A wait of" in str(bot_error):
                    wait_time = int("".join(filter(str.isdigit, str(bot_error))))
                    await asyncio.sleep(wait_time + 5)  # الانتظار حسب المدة المطلوبة قبل المتابعة
                failed_list.append(f"{bot_username} ({bot_error})")

        response = "✅ تمت إضافة البوتات بنجاح:\n" + "\n".join(success_list) if success_list else "❌ لم يتم إضافة أي بوت."
        if failed_list:
            response += "\n\n⚠️ فشل في إضافة بعض البوتات:\n" + "\n".join(failed_list)

        await event.reply(response)

    except Exception as e:
        await event.reply(f'❌ حدث خطأ أثناء محاولة إضافة البوتات: {e}')

with client:
    client.run_until_disconnected()
