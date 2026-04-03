import telebot, re, json, os, requests
from urllib.parse import urlparse, parse_qs
from telebot import types

TOKEN = '8592635991:AAFEvUQNHegCgONCX2Ko__TePQIUMi-ih0E'
CHANNEL_ID = '-1003762831847'
CHANNEL_NAME = '@xFlyZ1x'
ADMINS = {5453653945: "@l5ixi5l", 5140787805: "@Winter_grab"}
bot = telebot.TeleBot(TOKEN)
STATS_FILE = "stats.json"

def check_proxy(server, port):
    try:
        requests.get(f"http://{server}:{port}", timeout=2)
        return True
    except:
        return True

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f: return json.load(f)
        except: pass
    return {str(uid): 0 for uid in ADMINS}

def save_stats(stats):
    with open(STATS_FILE, "w") as f: json.dump(stats, f)

def format_and_post(url, message):
    try:
        clean_url = url.replace("tg://", "https://t.me/")
        p = urlparse(clean_url)
        q = parse_qs(p.query)
        s = q.get('server',[''])[0]
        port = q.get('port',[''])[0]
        sec = q.get('secret',[''])[0]
        bot.send_message(message.chat.id, f"⏳ Проверяю {s}...")
        if check_proxy(s, port):
            final_url = f"https://t.me/proxy?server={s}&port={port}&secret={sec}"
            text = f"<b>{CHANNEL_NAME}</b>\n#прокси\n\n<b>Сервер:</b> <code>{s}</code>\n<b>Порт:</b> <code>{port}</code>\n<b>Ключ:</b> <code>{sec}</code>\n"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="⚡ ПОДКЛЮЧИТЬ", url=final_url))
            bot.send_message(CHANNEL_ID, text, parse_mode='HTML', reply_markup=markup)
            stats = load_stats()
            uid = str(message.from_user.id)
            stats[uid] = stats.get(uid, 0) + 1
            save_stats(stats)
            bot.reply_to(message, f"✅ Опубликовано! Счет: {stats[uid]}")
        else:
            bot.reply_to(message, "❌ Прокси МЕРТВ.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['start', 'stats'])
def handle_commands(message):
    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "Извините, вы не админ канала @xFlyZ1x...😮"); return
    if message.text == "/stats":
        stats = load_stats()
        res = "<b>📊 Статистика админов:</b>\n\n"
        for aid, nick in ADMINS.items():
            res += f"👤 {nick}: {stats.get(str(aid), 0)} шт.\n"
        bot.send_message(message.chat.id, res, parse_mode='HTML')
    else:
        bot.reply_to(message, "Здарова! Кидай прокси или /stats")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "Извините, вы не админ канала @xFlyZ1x...😮"); return
    txt = message.text or ""
    links = re.findall(r'(https://t\.me/proxy\?[\w=&%.-]+|tg://proxy\?[\w=&%.-]+)', txt)
    if links:
        format_and_post(links[0], message)
    elif message.entities:
        for entity in message.entities:
            if entity.type == 'text_link' and ("t.me/proxy?" in entity.url or "tg://proxy?" in entity.url):
                format_and_post(entity.url, message)
                return
    else:
        bot.reply_to(message, "Пришли прокси или жми /stats")

bot.polling(none_stop=True)
