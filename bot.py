import os
import telebot

BOT_TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Используйте /all чтобы упомянуть всех.")

@bot.message_handler(commands=['all'])
def all_cmd(message):
    bot.send_message(message.chat.id, "Тегаю всех\n@mxvsatv @dnodnahadnedna @komi2021 @san_dor_ka @khopunovvv @Da1syBell @normal35235 @prowess100 @DaveTokami @m1st777 @Kastyay")

print("✅ Бот запущен на Railway!")
bot.polling(none_stop=True)
