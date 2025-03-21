from telethon import TelegramClient, events
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError, RpcCallFailError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUser

# بيانات البوت
API_ID = 123456  # ضع API_ID هنا
API_HASH = "your_api_hash_here"  # ضع API_HASH هنا

# قائمة معرفات البوتات (بالأرقام)
bot_ids = [
    7908156943, 1910015590
]

# إنشاء العميل (البوت)
bot = TelegramClient("bot_session", API_ID, API_HASH)
@bot.on(events.NewMessage(pattern="/addbots"))
async def add_bots(event):
    chat = await event.get_chat()  # الحصول على معلومات المجموعة
    if not event.is_group:  # التحقق إذا كان الأمر داخل مجموعة
        await event.reply("❌ هذا الأمر يعمل فقط في المجموعات.")
        return

    added_count = 0
    failed_bots = []

    for bot_id in bot_ids:
        try:
            user = await bot(GetFullUserRequest(bot_id))  # جلب معلومات البوت
            input_user = InputUser(user.user.id, user.user.access_hash)  # تحويله إلى كائن مستخدم
            await bot(InviteToChannelRequest(chat, [input_user]))  # دعوة البوت للمجموعة
            added_count += 1
            await event.reply(f"✅ تمت إضافة البوت {bot_id} بنجاح!")
        except UserAlreadyParticipantError:
            await event.reply(f"⚠️ البوت {bot_id} موجود بالفعل في المجموعة.")
        except UserPrivacyRestrictedError:
            await event.reply(f"⛔ لا يمكن إضافة البوت {bot_id} بسبب إعدادات الخصوصية.")
        except RpcCallFailError:
            await event.reply(f"🚫 فشل استدعاء API عند محاولة إضافة {bot_id}.")
        except Exception as e:
            failed_bots.append(bot_id)
            await event.reply(f"❌ خطأ أثناء إضافة البوت {bot_id}: {str(e)}")

    await event.reply(f"✅ تم إضافة {added_count} بوتات بنجاح!")
    
    if failed_bots:
        await event.reply(f"⚠️ لم يتمكن البوت من إضافة {len(failed_bots)} بوتات: {', '.join(map(str, failed_bots))}")

print("✅ البوت يعمل بنجاح!")
bot.run_until_disconnected()
