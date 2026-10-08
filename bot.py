import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ВСТАВЬТЕ СЮДА ВАШ ТОКЕН ОТ BOTFATHER
TOKEN = "8953531731:AAFaVxf-gFzMFC6jqC4lMViSgyWiNA83RU4"

# ВСТАВЬТЕ СЮДА ВАШ TELEGRAM ID (узнать можно через @userinfobot)
ADMIN_ID = 694392046

# ВСТАВЬТЕ СЮДА ССЫЛКУ НА ОПЛАТУ
PAYMENT_LINK = "https://securepayecom.com/sc/tqudmpUtBwVuCdVv"

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте! Это бот проекта «Удача на Байкале» 🌊 \n\n"
        "Чтобы участвовать в акции, вам нужно:\n"
        f"1. Оплатить постер по ссылке: {PAYMENT_LINK}\n"
        "2. Прислать сюда фото чека и ваше ФИО.\n\n"
        "После проверки мы присвоим вам номер и отправим постер."
    )
    await update.message.reply_text(text)

# Обработка текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Пожалуйста, пришлите фото чека и ваше ФИО.\n"
        "Без этого мы не сможем присвоить номер."
    )
    await update.message.reply_text(text)

# Обработка фото (чеков)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo_file = await update.message.photo
[-1].get_file()
    
    # Отправляем подтверждение пользователю
    await update.message.reply_text(
        "Спасибо! Ваш чек получен. Мы проверим оплату и присвоим вам номер.\n"
        "Ожидайте сообщения."
    )
    
    # Пересылаем фото и информацию админу
    caption = (
        f"Новый чек!\n"
        f"Пользователь: {user.full_name}\n"
        f"Юзернейм: @{user.username if user.username else 'нет'}\n"
        f"ID: {user.id
}"
    )
    
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_file.file_id,
        caption=caption
    )

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO
, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
