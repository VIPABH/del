from telethon import TelegramClient, events
import os, asyncio, random, time
from faker import Faker 

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

if not all([api_id, api_hash, bot_token]):
    raise ValueError("الرجاء ضبط المتغيرات البيئية API_ID, API_HASH، و BOT_TOKEN")

ABH = TelegramClient("code", api_id, api_hash).start(bot_token=bot_token)
res = {}
a = 0
players = {}
answer = None
is_on = False
join_on = False
start_time = None
done = False
fake = Faker("ar_AA")
@ABH.on(events.NewMessage(pattern="(?i)اسرع$"))
async def start_s(event):
    """بدء اللعبة والإعلان عنها"""
    global is_on, players
    is_on = True
    players.clear()
    uid = event.sender_id
    sender = await event.get_sender()
    name = sender.first_name
    if uid not in players:
         players[uid] = {"username": name}
         res[name] = {"name": name, "score": 0}
         await event.reply("اهلاً ضفتك للعبة , للانضمام ارسل `انا` للبدء `تم` \n**ENJOY BABY✌**")
@ABH.on(events.NewMessage(pattern="(?i)انا$"))
async def sign_in(event):
    if is_on:
        uid = event.sender_id
        sender = await event.get_sender()
        name = sender.first_name
        if uid not in players:
            players[uid] = {"username": name}
            res[name] = {"name": name, "score": 0}
            await event.reply('سجلتك باللعبة، لا ترسل مجددًا!')
        else:
            await event.reply("عزيزي الصديق، سجلتك والله!")
@ABH.on(events.NewMessage(pattern="(?i)الاعبين$"))
async def players_show(event):
    global is_on
    if is_on and players:
        player_list = "\n".join([f"{pid} - {info['username']}" for pid, info in players.items()])
        await event.reply(f"📜 قائمة اللاعبين:\n{player_list}")
        is_on = True
    else:
        await event.reply('ماكو لاعبين 🙃')
        is_on = False
@ABH.on(events.NewMessage(pattern="(?i)تم$"))
async def start_f(event):
    global answer, is_on, start_time, join_on
    join_on = True
    done = True
    if is_on and done and players:
        await event.reply('تم بدء اللعبة، انتظر ثواني...')
        done = True
        await asyncio.sleep(2)
        for _ in range(5):
            word = fake.word()
            answer = (word)
            await event.respond(f'✍ اكتب ⤶ {answer}')
            start_time = time.time()
            await asyncio.sleep(10)
        is_on = False
        done = False
        points_list = "\n".join([f"{info['name']} - {info['score']} نقطة" for info in res.values()])
        await event.reply(f"**ترتيب اللاعبين بالنقاط**\n{points_list}")
@ABH.on(events.NewMessage)
async def check(event):
    global is_on, start_time, answer, a, join_on
    join_on = False
    if not is_on or start_time is None:
        return
    elapsed_time = time.time() - start_time
    seconds = int(elapsed_time)
    milliseconds = int((elapsed_time - seconds) * 1000)
    isabh = event.text.strip()
    wid = event.sender_id
    if answer and isabh.lower() == answer.lower() and wid in players:
        username = players[wid]["username"]
        if username not in res:
            res[username] = {"name": username, "score": 0}
        res[username]["score"] += 1
        await event.reply(f'إجابة صحيحة! أحسنت الوقت المستغرق: {seconds} ثانية و {milliseconds} مللي ثانية.')
        is_on = False
        answer = None
        start_time = None
    elif elapsed_time >= 10:
        is_on = False
        answer = None
        start_time = None
        if a == 5:
            is_on = False
            points_list = "\n".join([f"{pid} -> {info['score']} نقطة" for pid, info in res.items()])
            await event.reply(f"**ترتيب اللاعبين بالنقاط**\n{points_list}")
ABH.run_until_disconnected()
