from telethon import TelegramClient, events
import os, asyncio, time

# تحميل القيم من البيئة
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

# إنشاء العميل باستخدام API ID و API Hash وتوكن البوت
ABH = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)

# قاموس لتخزين معلومات المستخدمين
uinfo = {}

# التعامل مع الرسائل الجديدة
@ABH.on(events.NewMessage)
async def msgs(event):
    global uinfo
    if event.is_group:
        uid = event.sender.first_name  # الاسم الأول للمستخدم
        unm = event.sender_id  # ID المستخدم
        guid = event.chat_id  # ID المجموعة
        # تحديث عدد الرسائل التي أرسلها المستخدم في هذه المجموعة
        uinfo.setdefault(unm, {}).setdefault(guid, {"guid": guid, "unm": unm, "fname": uid, "msg": 0})["msg"] += 1

# التعامل مع الأمر 'توب'
@ABH.on(events.NewMessage(pattern='توب'))
async def show_res(event):
    await asyncio.sleep(2)  # الانتظار قليلاً
    guid = event.chat_id  # ID المجموعة
    sorted_users = sorted(uinfo.items(), key=lambda x: x[1][guid]['msg'], reverse=True)[:15]  # ترتيب المستخدمين حسب عدد الرسائل
    top_users = []
    for user, data in sorted_users:
        if guid in data:
            top_users.append(f"{data[guid]['msg']} رسائل")
    if top_users:
        await event.reply("\n".join(top_users))  # إرسال قائمة أعلى 15 مستخدم
    else:
        await event.reply("لا توجد بيانات لعرضها.")

# التعامل مع الأمر 'رسائلي' لعرض عدد الرسائل الخاصة بالمستخدم في المجموعة
@ABH.on(events.NewMessage(pattern='رسائلي'))
async def show_res(event):
    await asyncio.sleep(2)
    uid1 = event.sender.first_name
    unm1 = event.sender_id
    guid1 = event.chat_id
    if unm1 in uinfo and guid1 in uinfo[unm1]:
        msg_count = uinfo[unm1][guid1]["msg"]
        await event.reply(f"المستخدم [{uid1}](tg://user?id={unm1}) أرسلت {msg_count} رسالة في هذه المجموعة.")

# التعامل مع الردود لعرض عدد الرسائل المرسلة من المستخدم المحدد في الرد
@ABH.on(events.NewMessage(pattern='رسائله|رسائلة|رسائل|الرسائل'))
async def show_res(event):
    r = await event.get_reply_message()  # الحصول على الرسالة المردود عليها
    await asyncio.sleep(2)
    if not r:  # إذا لم يكن هناك رد، لا نفعل شيئاً
        return
    uid1 = r.sender.first_name
    unm1 = r.sender_id
    guid1 = event.chat_id
    if unm1 in uinfo and guid1 in uinfo[unm1]:
        msg_count = uinfo[unm1][guid1]["msg"]
        await event.reply(f"المستخدم [{uid1}](tg://user?id={unm1}) أرسل {msg_count} رسالة في هذه المجموعة.")

# التعامل مع الأمر '/الرسائل' لعرض أوامر البوت
@ABH.on(events.NewMessage(pattern='/الرسائل'))
async def title(event):
    await event.reply('اهلا صديقي , اوامر الرسائل \n ارسل `توب` ل اضهار توب 15 تفاعل \n ارسل `رسائلي` ل اضهار رسائلك في اخر يوم \n ارسل `رسائله` ل اضهار رساله الشخص بالرد \n استمتع')

# بدء البوت
ABH.run_until_disconnected()
