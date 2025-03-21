from telethon import TelegramClient, events
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError, RpcCallFailError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUser

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH') 
# قائمة معرفات البوتات (بالأرقام)
bot_ids = [7908156943, 1910015590]

# إنشاء العميل (تسجيل الدخول عبر رقم الهاتف)
bot = TelegramClient("user_session", API_ID, API_HASH)

async def main():
    await bot.start(PHONE_NUMBER)  # تسجيل الدخول برقم الهاتف
    print("✅ تم تسجيل الدخول بنجاح!")

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
            user = await bot(GetFullUserRequest(str(bot_id)))  # جلب معلومات البوت
            input_user = InputUser(user.user.id, user.user.access_hash)  # تحويله إلى كائن مستخدم
            await bot(InviteToChannelRequest(chat, [input_user]))  # دعوة البوت للمجموعة
            added_count += 1
        except UserAlreadyParticipantError:
            failed_bots.append(f"⚠️ البوت {bot_id} موجود بالفعل.")
        except UserPrivacyRestrictedError:
            failed_bots.append(f"⛔ لا يمكن إضافة {bot_id} (إعدادات الخصوصية).")
        except RpcCallFailError:
            failed_bots.append(f"🚫 فشل استدعاء API عند محاولة إضافة {bot_id}.")
        except Exception as e:
            failed_bots.append(f"❌ خطأ في {bot_id}: {str(e)}")

    if added_count > 0:
        await event.reply(f"✅ تم إضافة {added_count} بوتات بنجاح!")

    if failed_bots:
        await event.reply("\n".join(failed_bots))

print("✅ جاري تشغيل البوت...")
bot.loop.run_until_complete(main())
bot.run_until_disconnected()
