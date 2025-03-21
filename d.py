from telethon import TelegramClient, events
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError, RpcCallFailError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUser
import os
import asyncio

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = "+964 770 598 4153"
bot_usernames = ["@VIPABH_BOT"]

bot = TelegramClient("user_session", API_ID, API_HASH)

async def main():
    await bot.start(PHONE_NUMBER)

@bot.on(events.NewMessage(pattern="/addbots"))
async def add_bots(event):
    if not event.is_group:
        await event.reply("❌ يعمل فقط في المجموعات.")
        return
    chat = await event.get_chat()
    added_count = 0
    failed_bots = []

    for bot_username in bot_usernames:
        try:
            user_full = await bot(GetFullUserRequest(bot_username))
            user = user_full.user
            if not user.bot:
                failed_bots.append(f"⛔ {bot_username} ليس بوتًا.")
                continue
            input_user = InputUser(user.id, user.access_hash)
            await bot(InviteToChannelRequest(chat, [input_user]))
            added_count += 1
        except (UserAlreadyParticipantError, UserPrivacyRestrictedError, RpcCallFailError, FloodWaitError) as e:
            failed_bots.append(f"❌ فشل في إضافة {bot_username}: {str(e)}")

    if added_count > 0:
        await event.reply(f"✅ تم إضافة {added_count} بوت بنجاح!")
    if failed_bots:
        await event.reply("\n".join(failed_bots))

bot.loop.run_until_complete(main())
bot.run_until_disconnected()
