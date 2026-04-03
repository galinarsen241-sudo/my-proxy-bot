import telebot
from urllib.parse import urlparse, parse_qs

# Настройки
bot = telebot.TeleBot('8592635991:AAFEvUQNHegCgONCX2Ko__TePQIUMi-ih0E')
CHANNEL_ID = '-1003762831847' # Например @pelmeshki_flyz
CHANNEL_NAME = '@xFlyZ1x'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Пришли мне ссылку на прокси (t.me/proxy...), и я опубликую её красиво!")

@bot.message_handler(func=lambda m: "t.me/proxy?" in m.text)
def handle_proxy(message):
    try:
        # Парсим ссылку
        url = message.text.strip()
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        server = params.get('server', [''])[0]
        port = params.get('port', [''])[0]
        secret = params.get('secret', [''])[0]

        # Оформляем текст как на твоем фото
        text = (
            f"<b>{CHANNEL_NAME}</b>\n"
            f"#прокси\n\n"
            f"<b>Сервер:</b> <code>{server}</code>\n"
            f"<b>Порт:</b> <code>{port}</code>\n"
            f"<b>Ключ:</b> <code>{secret}</code>\n\n"
            f"<blockquote>{url}</blockquote>"
        )

        # Публикуем в канал
        bot.send_message(CHANNEL_ID, text, parse_mode='HTML')
        bot.reply_to(message, "✅ Опубликовано в канал!")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

bot.polling()
