from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

# Включим базовые логи
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN = '6564742799:AAHMDMyFj3uSo3-X3M9WukvsnBWyNY9TXfU'

def start(update: Update, context):
    user_id = update.message.from_user.id
    if user_id == 170663702:
        keyboard = [
            [InlineKeyboardButton("Создать нового клиента", callback_data='create_client')],
            [InlineKeyboardButton("Перезагрузка сервера", callback_data='reboot_server')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
    else:
        update.message.reply_text('У вас нет доступа к этим функциям.')

def button(update: Update, context):
    query = update.callback_query
    if query.data == 'create_client':
        # TODO: Добавьте код для создания нового клиента
        query.edit_message_text(text="Клиент создан!")
    elif query.data == 'reboot_server':
        # TODO: Добавьте код для перезагрузки сервера
        query.edit_message_text(text="Сервер перезагружается!")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

