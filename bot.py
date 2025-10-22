import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Токен бота
BOT_TOKEN = '8443886410:AAECQfMTX4wVf0Ax1zkbVoqDbcUtMVTZIQU'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для упоминания всех участников. "
        "Добавьте меня в группу и дайте права администратора, "
        "затем используйте команду /all"
    )

async def all_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    try:
        # Проверяем, что команда используется в группе
        if update.effective_chat.type not in ['group', 'supergroup']:
            await update.message.reply_text("❌ Эта команда работает только в группах!")
            return
        
        await update.message.reply_text("⏳ Собираю список участников...")
        
        # Собираем уникальных пользователей
        unique_users = {}
        
        # Метод 1: Получаем администраторов
        try:
            admins = await context.bot.get_chat_administrators(chat_id)
            for admin in admins:
                user = admin.user
                if not user.is_bot and user.id not in unique_users:
                    unique_users[user.id] = user
        except Exception as e:
            print(f"Ошибка при получении администраторов: {e}")
        
        # Метод 2: Получаем пользователей из истории сообщений
        try:
            async for message in context.bot.get_chat_history(chat_id, limit=200):
                if message.from_user and not message.from_user.is_bot:
                    user = message.from_user
                    if user.id not in unique_users:
                        unique_users[user.id] = user
        except Exception as e:
            print(f"Ошибка при получении истории: {e}")
        
        # Формируем список упоминаний
        mentions = []
        for user in unique_users.values():
            if user.username:
                mentions.append(f"@{user.username}")
            else:
                # Если нет username, используем имя + ID для упоминания
                mentions.append(f"[{user.first_name or 'User'}](tg://user?id={user.id})")
        
        if mentions:
            # Разбиваем на группы по 20 упоминаний, чтобы не превысить лимит сообщения
            chunk_size = 20
            mention_chunks = [mentions[i:i + chunk_size] for i in range(0, len(mentions), chunk_size)]
            
            for i, chunk in enumerate(mention_chunks):
                message = f"📢 Участники ({len(mentions)} всего):\n" + " ".join(chunk) if i == 0 else " ".join(chunk)
                await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Не удалось найти участников для упоминания")
            
    except Exception as e:
        error_msg = f"❌ Ошибка: {str(e)}"
        if "Forbidden" in str(e):
            error_msg += "\n\nУбедитесь, что бот является администратором группы с правами:\n• Просмотр участников\n• Чтение истории сообщений"
        await update.message.reply_text(error_msg)

async def main():
    # Создаем Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("all", all_members))
    
    # Запускаем бота
    print("✅ Бот запущен и готов к работе!")
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
