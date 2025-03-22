from telethon import events

# وظيفة لحدث عند تلقي رسالة تحتوي على أمر
async def handle_commands(client):
    @abh.on(events.NewMessage(pattern='/start'))
    async def start_command(event):
        await event.reply("مرحبًا! أنا بوت تليجرام.")
