from telethon import events

# وظيفة لرد على الرسائل
async def reply_to_messages(client):
    @abh.on(events.NewMessage)
    async def handler(event):
        if 'مرحبًا' in event.raw_text:
            await event.reply('أهلاً وسهلاً!')
