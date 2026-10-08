import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8953531731:AAFaVxf-gFzMFC6jqC4lMViSgyWiNA83RU4"
ADMIN_IDS = [694392046, 8527096621]
PAYMENT_LINK = "https://securepayecom.com/sc/tqudmpUtBwVuCdVv"

# Хранилище уже обработанных чеков
processed_checks = set()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте! Это бот проекта «Удача на Байкале» 🌊\n\n"
        "Чтобы участвовать в акции, вам нужно:\n"
        "1. Оплатить постер по ссылке: " + PAYMENT_LINK + "\n"
        "2. Прислать сюда чек (фото или файлом) и ваше ФИО.\n\n"
        "После проверки мы присвоим вам номер и отправим постер."
    )
    await update.message.reply_text(text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Пожалуйста, пришлите чек (фото или файлом) и ваше ФИО.\n"
        "Без этого мы не сможем присвоить номер."
    )
    await update.message.reply_text(text)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    file_id = photo_file.file_id

    if file_id in processed_checks:
        await update.message.reply_text(
            "Этот чек уже был получен ранее. Пожалуйста, не отправляйте его повторно.\n"
            "Если вы оплатили новый постер — пришлите новый чек."
        )
        return

    processed_checks.add(file_id)

    await update.message.reply_text(
        "Спасибо! Ваш чек получен. Мы проверим оплату и присвоим вам номер.\n"
        "Ожидайте сообщения."
    )
    caption = (
        "Новый чек (фото)!\n"
        "Пользователь: " + user.full_name + "\n"
        "Ссылка на профиль: tg://user?id=" + str(user.id)
    )
    for admin_id in ADMIN_IDS:
        await context.bot.send_photo(
            chat_id=admin_id,
            photo=file_id,
            caption=caption
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    document = update.message.document
    file_id = document.file_id

    if file_id in processed_checks:
        await update.message.reply_text(
            "Этот чек уже был получен ранее. Пожалуйста, не отправляйте его повторно.\n"
            "Если вы оплатили новый постер — пришлите новый чек."
        )
        return

    processed_checks.add(file_id)

    await update.message.reply_text(
        "Спасибо! Ваш чек получен. Мы проверим оплату и присвоим вам номер.\n"
        "Ожидайте сообщения."
    )
    caption = (
        "Новый чек (файл)!\n"
        "Пользователь: " + user.full_name + "\n"
        "Ссылка на профиль: tg://user?id=" + str(user.id) + "\n"
        "Имя файла: " + document.file_name
    )
    for admin_id in ADMIN_IDS:
        await context.bot.send_document(
            chat_id=admin_id,
            document=file_id,
            caption=caption
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
