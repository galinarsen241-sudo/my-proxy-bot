import telebot, re, requests
from flask import Flask
from threading import Thread
from urllib.parse import urlparse, parse_qs
from telebot import types

server = Flask('')
@server.route('/')
def home():
    return "", 200
def run():
    server.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = '8592635991:AAFEvUQNHegCgONCX2Ko__TePQIUMi-ih0E'
CHANNEL_ID = '-1003762831847'
CHANNEL_NAME = '@xFlyZ1x'
ADMINS = [5453653945, 5140787805]
bot = telebot.TeleBot(TOKEN)

def check_proxy(server, port):
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((server, int(port)))
        s.close()
        return True
    except: return False

def format_and_post(url, message):
    try:
        clean_url = url.replace("tg://", "https://t.me/")
        p = urlparse(clean_url)
        q = parse_qs(p.query)
        s = q.get('server',[''])[0]
        port = q.get('port',[''])[0]
        sec = q.get('secret',[''])[0]
        bot.send_message(message.chat.id, f"⏳ Проверяю сервер, сэр {s}...")
        if check_proxy(s, port):
            final_url = f"https://t.me/proxy?server={s}&port={port}&secret={sec}"
            text = f"<b>{CHANNEL_NAME}</b>\n#прокси\n\n<b>Сервер:</b> <code>{s}</code>\n<b>Порт:</b> <code>{port}</code>\n<b>Ключ:</b> <code>{sec}</code>\n"
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text="⚡ ПОДКЛЮЧИТЬ", url=final_url))
            bot.send_message(CHANNEL_ID, text, parse_mode='HTML', reply_markup=markup)
            bot.reply_to(message, "✅ Прокси опубликован, сэр!")
        else:
            bot.reply_to(message, "❌ Этот прокси недоступен, сэр. Я не стал его публиковать.")
    except Exception as e:
        bot.reply_to(message, f"❌ Произошла ошибка, сэр: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in ADMINS:
        bot.reply_to(message, "Слушаю вас, сэр! Пришлите прокси для публикации.")
    else:
        bot.reply_to(message, "Извините, вы не админ канала @xFlyZ1x...😮")

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
            if entity.type == 'text_link' and ("proxy?" in entity.url):
                format_and_post(entity.url, message)
                return
    else:
        bot.reply_to(message, "Я ожидаю ссылку на прокси, сэр!")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
