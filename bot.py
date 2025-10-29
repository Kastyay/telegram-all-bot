import telebot
from telebot import types

BOT_TOKEN = '8443886410:AAECQfMTX4wVf0Ax1zkbVoqDbcUtMVTZIQU'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Бот для упоминания администраторов. Используйте /all в группе")

@bot.message_handler(commands=['all'])
def all_admins(message):
    try:
        # Проверяем, что команда вызвана в группе
        if message.chat.type not in ['group', 'supergroup']:
            bot.reply_to(message, "❌ Эта команда работает только в группах!")
            return
        
        chat_id = message.chat.id
        
        # Получаем список администраторов
        admins = bot.get_chat_administrators(chat_id)
        
        # Формируем список упоминаний администраторов
        admin_mentions = []
        for admin in admins:
            user = admin.user
            # Пропускаем ботов
            if not user.is_bot:
                if user.username:
                    # Если есть username, упоминаем по нему
                    admin_mentions.append(f"@{user.username}")
                else:
                    # Если нет username, используем ID для упоминания
                    admin_mentions.append(f'<a href="tg://user?id={user.id}">{user.first_name}</a>')
        
        if admin_mentions:
            # Собираем сообщение
            response = "👥 Администраторы группы:\n" + " ".join(admin_mentions)
            bot.send_message(chat_id, response, parse_mode='HTML')
        else:
            bot.reply_to(message, "❌ Не удалось найти администраторов")
            
    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        if "Forbidden" in str(e):
            error_msg += "\n\nУбедитесь, что бот является администратором группы!"
        bot.reply_to(message, error_msg)

print("✅ Бот запущен и готов тегать администраторов!")
bot.polling(none_stop=True)
