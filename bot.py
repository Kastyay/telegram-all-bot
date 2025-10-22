import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Токен бота
BOT_TOKEN = '8443886410:AAECQfMTX4wVf0Ax1zkbVoqDbcUtMVTZIQU'

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Привет! Я бот для упоминания всех участников. "
        "Добавьте меня в группу и дайте права администратора, "
        "затем используйте команду /all"
    )

def all_members(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    try:
        # Проверяем, что команда используется в группе
        if update.effective_chat.type not in ['group', 'supergroup']:
            update.message.reply_text("Эта команда работает только в группах!")
            return
        
        # Получаем информацию о чате
        chat = context.bot.get_chat(chat_id)
        total_members = chat.get_member_count()
        
        update.message.reply_text(f"⏳ Собираю список участников ({total_members} человек)...")
        
        # Получаем администраторов (самый простой способ получить список участников)
        administrators = context.bot.get_chat_administrators(chat_id)
        
        # Формируем список упоминаний
        mentions = []
        for admin in administrators:
            user = admin.user
            # Пропускаем ботов
            if not user.is_bot:
                if user.username:
                    mentions.append(f"@{user.username}")
                else:
                    mentions.append(f"[{user.first_name}](tg://user?id={user.id})")
        
        # Отправляем сообщение
        if mentions:
            message = f"📢 Внимание всем! ({len(mentions)} участников)\n" + " ".join(mentions)
            if len(message) > 4096:
                # Если сообщение слишком длинное, разбиваем на части
                parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
                for part in parts:
                    update.message.reply_text(part, parse_mode='Markdown')
            else:
                update.message.reply_text(message, parse_mode='Markdown')
        else:
            update.message.reply_text("📢 Внимание всем! @all")
            
    except Exception as e:
        update.message.reply_text(f"Ошибка! Убедитесь, что бот является администратором группы. Детали: {str(e)}")

def main():
    # Создаем updater и dispatcher
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Добавляем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("all", all_members))
    
    # Запускаем бота
    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
