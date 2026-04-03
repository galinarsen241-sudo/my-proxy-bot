import telebot
from urllib.parse import urlparse, parse_qs

TOKEN = '8592635991:AAFEvUQNHegCgONCX2Ko__TePQIUMi-ih0E'
CHANNEL_ID = '-1003762831847'
CHANNEL_NAME = '@xFlyZ1x'

# Список разрешенных ID (Ты и твой друг)
ADMINS = [5453653945, 5140787805]

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
 if message.from_user.id in ADMINS:
  bot.reply_to(message, "Привет, админ! Я готов к работе. Кидай ссылку.")
 else:
  bot.reply_to(message, "э иди атсбда нафек какашка этим ботом управляют только админы @xFlyZ1x")

@bot.message_handler(func=lambda m: True) # Слушаем все сообщения
def handle_all(message):
 # Проверяем, админ ли это
 if message.from_user.id not in ADMINS:
  bot.reply_to(message, "э иди атсбда нафек какашка этим ботом управляют только админы @xFlyZ1x")
  return

 # Если это админ и он прислал ссылку на прокси
 if message.text and "t.me/proxy?" in message.text:
  try:
   url = message.text.strip()
   p = urlparse(url)
   q = parse_qs(p.query)
   s = q.get('server',[''])[0]
   port = q.get('port',[''])[0]
   sec = q.get('secret',[''])[0]
   
   text = f"<b>{CHANNEL_NAME}</b>\n#прокси\n\n<b>Сервер:</b> <code>{s}</code>\n<b>Порт:</b> <code>{port}</code>\n<b>Ключ:</b> <code>{sec}</code>\n\n<blockquote>{url}</blockquote>"
   
   bot.send_message(CHANNEL_ID, text, parse_mode='HTML')
   bot.reply_to(message, "✅ Опубликовано, босс!")
  except Exception as e:
   bot.reply_to(message, f"❌ Ошибка: {e}")
 else:
  bot.reply_to(message, "Я жду ссылку на прокси, бро!")

print("Бот с защитой запущен...")
bot.polling(none_stop=True)
