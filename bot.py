import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get('8443886410:AAECQfMTX4wVf0Ax1zkbVoqDbcUtMVTZIQU')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для упоминания всех участников. "
        "Добавьте меня в группу и дайте права администратора, "
        "затем используйте команду /all"
    )

async def all_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot
    
    try:
        # Проверяем, что команда используется в группе
        if update.effective_chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("Эта команда работает только в группах!")
            return
        
        # Получаем информацию о чате
        chat = await bot.get_chat(chat_id)
        total_members = chat.get_member_count()
        
        await update.message.reply_text(f"⏳ Собираю список участников ({total_members} человек)...")
        
        # Собираем уникальных участников из последних сообщений
        unique_users = set()
        try:
            # Получаем последние сообщения (максимум 100)
            async for message in bot.get_chat_history(chat_id, limit=100):
                if message.from_user and not message.from_user.is_bot:
                    user = message.from_user
                    if user.username:
                        unique_users.add(f"@{user.username}")
                    else:
                        unique_users.add(f"[{user.first_name}](tg://user?id={user.id})")
        except Exception as e:
            print(f"Ошибка при получении истории: {e}")
        
        # Если удалось собрать участников
        if unique_users:
            message = f"📢 Внимание всем! ({len(unique_users)} участников)\n" + " ".join(list(unique_users))
            # Разбиваем на части если сообщение слишком длинное
            if len(message) > 4096:
                parts = [message[i:i+4096] for i in range(0, len(message), 4096)]
                for part in parts:
                    await update.message.reply_text(part, parse_mode='Markdown')
            else:
                await update.message.reply_text(message, parse_mode='Markdown')
        else:
            # Альтернатива - просто отправить @all
            await update.message.reply_text("📢 Внимание всем! @all")
            
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

def main():
    if not BOT_TOKEN:
        print("Ошибка: BOT_TOKEN не установлен!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("all", all_members))
    
    print("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()