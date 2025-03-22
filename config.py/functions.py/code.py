import random

@ABH.on(events.NewMessage(pattern=r'^مخفي$'))
async def reply(event):
    if event.is_reply:
        return
    vipabh = random.choice(abh)
    if vipabh.startswith("http"):
        await event.reply(file=vipabh)
    else:
        await event.reply(vipabh)
@ABH.on(events.NewMessage(pattern='ابن هاشم'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        rl = random.randint(1222, 1241)
        url = f"https://t.me/VIPABH/{rl}"
        caption = "أبن هاشم (رض) مرات متواضع ،🌚 @K_4x1"
        button = [Button.url(text="الking", url="https://t.me/K_4x1")]
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id, buttons=button)
    else:
        return
@ABH.on(events.NewMessage(pattern='زهراء'))
async def reply_abh(event):
    if event.chat_id == -1001968219024:
        url = "https://t.me/VIPABH/1220"  
        caption = "@klix_78 ( لَقَدْ كَفَرَ الّذِينَ قَالُوا إنَّ الله هُو المَسِيحُ ابْنُ مَرْيَم)." 
        await event.client.send_file(event.chat_id, url, caption=caption, reply_to=event.message.id)    
    else: 
        return


now = datetime.now()
hour = now.hour
m = now.minute
print(f'anymous is working at {hour}:{m} ✓')
