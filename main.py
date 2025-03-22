import asyncio
from config import start_bot, reply_to_messages, handle_commands

async def main():
    # استيراد client من config
    from config.abh import client
    
    # بدء البوت
    await start_bot()
    
    # تشغيل الوظائف الأخرى مثل الرد على الرسائل أو التعامل مع الأوامر
    await reply_to_messages(client)
    await handle_commands(client)

asyncio.run(main())
