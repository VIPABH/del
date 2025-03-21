from telethon import TelegramClient, events
from telethon.errors import UserPrivacyRestrictedError, UserAlreadyParticipantError, RpcCallFailError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputUser
import os
import asyncio  # استيراد مكتبة asyncio لتأخير غير متزامن

API_ID = os.getenv('API_ID')      
API_HASH = os.getenv('API_HASH')
PHONE_NUMBER = "+964 770 598 4153"
bot_usernames = ["@VIPABH_BOT", "@D7Bot"]

# إنشاء العميل (تسجيل الدخول عبر رقم الهاتف)
bot = TelegramClient("user_session", API_ID, API_HASH)

async def main():
    await bot.start(PHONE_NUMBER)  # تسجيل الدخول برقم الهاتف
    print("✅ تم تسجيل الدخول بنجاح!")

@bot.on(events.NewMessage(pattern="/addbots"))
async def add_bots(event):
    if not event.is_group:  # التحقق إذا كان الأمر داخل مجموعة
        await event.reply("❌ هذا الأمر يعمل فقط في المجموعات.")
        return

    chat = await event.get_chat()  # الحصول على معلومات المجموعة
    added_count = 0
    failed_bots = []

    # استخدام bot_usernames بدلاً من bot_ids
    for bot_username in bot_usernames:
        try:
            user_full = await bot(GetFullUserRequest(bot_username))  # جلب معلومات البوت
            user = user_full.user  # الوصول إلى المستخدم من UserFull

            # التأكد من أن المستخدم هو بوت وليس حساب شخصي
            if not user.bot:
                failed_bots.append(f"⛔ {bot_username} ليس بوتًا.")
                continue

            input_user = InputUser(user.id, user.access_hash)  # تحويله إلى كائن مستخدم
            await bot(InviteToChannelRequest(chat, [input_user]))  # دعوة البوت للمجموعة
            added_count += 1
        except UserAlreadyParticipantError:
            failed_bots.append(f"⚠️ البوت {bot_username} موجود بالفعل.")
        except UserPrivacyRestrictedError:
            failed_bots.append(f"⛔ لا يمكن إضافة {bot_username} (إعدادات الخصوصية).")
        except RpcCallFailError:
            # محاولة إعادة استدعاء API بعد تأخير باستخدام asyncio
            failed_bots.append(f"🚫 فشل استدعاء API عند محاولة إضافة {bot_username}. سيتم المحاولة مرة أخرى.")
            await asyncio.sleep(2)  # تأخير غير متزامن قبل المحاولة مرة أخرى
            try:
                user_full = await bot(GetFullUserRequest(bot_username))  # إعادة المحاولة لجلب معلومات البوت
                user = user_full.user
                input_user = InputUser(user.id, user.access_hash)
                await bot(InviteToChannelRequest(chat, [input_user]))  # دعوة البوت للمجموعة
                added_count += 1
            except Exception as e:
                failed_bots.append(f"❌ فشل في إضافة {bot_username} بعد المحاولة الثانية: {str(e)}")
        except FloodWaitError as e:
            failed_bots.append(f"⏳ هناك انتظار لعدة دقائق بسبب كثرة الطلبات: {e.seconds} ثانية.")
            await asyncio.sleep(e.seconds)  # الانتظار بناءً على الوقت المقدر
        except Exception as e:
            failed_bots.append(f"❌ خطأ في {bot_username}: {str(e)}")

    if added_count > 0:
        await event.reply(f"✅ تم إضافة {added_count} بوتات بنجاح!")

    if failed_bots:
        await event.reply("\n".join(failed_bots))

print("✅ جاري تشغيل البوت...")
bot.loop.run_until_complete(main())
bot.run_until_disconnected()
