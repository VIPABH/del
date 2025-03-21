from telethon import TelegramClient, events
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError, RpcCallFailError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel
import os

# بيانات تسجيل الدخول
API_ID = int(os.getenv('API_ID', 123456))  # استبدل 123456 بـ API_ID الحقيقي
API_HASH = os.getenv('API_HASH', 'your_api_hash_here')  # استبدل 'your_api_hash_here' بـ API_HASH الحقيقي
PHONE_NUMBER = "+9647705984153"  # رقم الهاتف بدون مسافات

# قائمة أسماء المستخدمين للبوتات
bot_usernames = ["@VIPABH_BOT", "@D7Bot"]  

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

    for bot_username in bot_usernames:
        try:
            user = await bot.get_entity(bot_username)  # جلب معلومات البوت باستخدام @username
            # استخدام InputPeerChannel بدلاً من InputPeerChat
            input_channel = InputPeerChannel(chat.id, chat.access_hash)  # تحويل إلى InputPeerChannel
            await bot(InviteToChannelRequest(input_channel, [user]))  # دعوة البوت للمجموعة
            added_count += 1
        except UserAlreadyParticipantError:
            failed_bots.append(f"⚠️ البوت {bot_username} موجود بالفعل.")
        except UserPrivacyRestrictedError:
            failed_bots.append(f"⛔ لا يمكن إضافة {bot_username} (إعدادات الخصوصية).")
        except RpcCallFailError:
            failed_bots.append(f"🚫 فشل استدعاء API عند محاولة إضافة {bot_username}.")
        except Exception as e:
            failed_bots.append(f"❌ خطأ في {bot_username}: {str(e)}")

    if added_count > 0:
        await event.reply(f"✅ تم إضافة {added_count} بوتات بنجاح!")

    if failed_bots:
        await event.reply("\n".join(failed_bots))

print("✅ جاري تشغيل البوت...")
bot.loop.run_until_complete(main())
bot.run_until_disconnected()
