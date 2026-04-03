import telebot
import re
from urllib.parse import urlparse, parse_qs
from telebot import types # Добавили библиотеку кнопок

TOKEN = '8592635991:AAFEvUQNHegCgONCX2Ko__TePQIUMi-ih0E'
CHANNEL_ID = '-1003762831847'
CHANNEL_NAME = '@xFlyZ1x'
ADMINS = [5453653945, 5140787805]

bot = telebot.TeleBot(TOKEN)

def format_and_post(url, message):
    try:
        p = urlparse(url)
        q = parse_qs(p.query)
        s = q.get('server',[''])[0]
        port = q.get('port',[''])[0]
        sec = q.get('secret',[''])[0]
        
        text = (
            f"<b>{CHANNEL_NAME}</b>\n"
            f"#прокси\n\n"
            f"<b>Сервер:</b> <code>{s}</code>\n"
            f"<b>Порт:</b> <code>{port}</code>\n"
            f"<b>Ключ:</b> <code>{sec}</code>\n"
        )
        
        # Создаем красивую кнопку
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="⚡ ПОДКЛЮЧИТЬ", url=url)
        markup.add(btn)
        
        bot.send_message(CHANNEL_ID, text, parse_mode='HTML', reply_markup=markup)
        bot.reply_to(message, "✅ Опубликовал с кнопкой!")
    except:
        bot.reply_to(message, "❌ Ошибка в ссылке.")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    if message.from_user.id not in ADMINS:
        bot.reply_to(message, "э иди атсбда нафек какашка @xFlyZ1x")
        return

    links = re.findall(r'https://t\.me/proxy\?[\w=&%.-]+', message.text or "")
    if links:
        format_and_post(links[0], message)
    elif message.entities:
        for entity in message.entities:
            if entity.type == 'text_link' and "t.me/proxy?" in entity.url:
                format_and_post(entity.url, message)
                return
    else:
        bot.reply_to(message, "Пришли прокси, бро!")

bot.polling(none_stop=True)
