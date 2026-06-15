import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from rag_bot import retrieve, generate_answer

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN не задан в .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение"""
    await update.message.reply_text(
        "Привет! Я RAG-бот на основе локальной базы знаний.\n"
        "Задавай вопросы по вселенной Sailor Moon (с изменёнными именами).\n"
        "Если я не знаю ответа — честно скажу об этом."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    question = update.message.text.strip()
    if not question:
        await update.message.reply_text("Пожалуйста, введите вопрос.")
        return

    # Показываем статус печатает...
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # 1. Поиск чанков
        docs = retrieve(question, k=3)
        if not docs:
            await update.message.reply_text("Не нашёл информации по вашему запросу в базе знаний.")
            return

        # 2. Генерация ответа
        answer = generate_answer(question, docs)

        # 3. Формируем ответ с источниками
        sources = "\n".join([f"{d['source']} (score: {d['score']:.2f})" for d in docs])
        response = f"{answer}\n\nИсточники:\n{sources}"

        # Telegram ограничивает длину сообщения 4096 символами
        if len(response) > 4096:
            response = response[:4093] + "..."

        await update.message.reply_text(response)

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуйте позже.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()