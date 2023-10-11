from telegram import Bot, Update, ReplyKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import logging

# Включим базовые логи
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN = '6564742799:AAHMDMyFj3uSo3-X3M9WukvsnBWyNY9TXfU'

def start(update: Update, context):
    user_id = update.message.from_user.id
    if user_id == 170663702:
        keyboard = [
            [ReplyKeyboardButton("Создать нового клиента")],
            [ReplyKeyboardButton("Перезагрузка сервера")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
    else:
        update.message.reply_text('У вас нет доступа к этим функциям.')

def handle_message(update: Update, context):
    message_text = update.message.text
    if message_text == "Создать нового клиента":
        # TODO: Добавьте код для создания нового клиента
        update.message.reply_text("Клиент создан!")
    elif message_text == "Перезагрузка сервера":
        # TODO: Добавьте код для перезагрузки сервера
        update.message.reply_text("Сервер перезагружается!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

    main()

