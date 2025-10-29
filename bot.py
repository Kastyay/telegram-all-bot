import os
import telebot
from flask import Flask
from threading import Thread

# Простой веб-сервер для Render
app = Flask('')

@app.route('/')
def home():
    return "✅ Бот работает!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Запускаем веб-сервер в фоне
keep_alive()

# Код бота
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8443886410:AAECQfMTX4wVf0Ax1zkbVoqDbcUtMVTZIQU')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Используйте /all")

@bot.message_handler(commands=['all'])
def all_cmd(message):
    bot.send_message(message.chat.id, "Тегаю всех\n@mxvsatv @dnodnahadnedna @komi2021 @san_dor_ka @khopunovvv @Da1syBell @normal35235 @prowess100 @DaveTokami @m1st777 @Kastyay")

print("✅ Бот запущен!")
bot.polling(none_stop=True)
