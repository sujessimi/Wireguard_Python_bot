import os
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
import sqlite3
import datetime

# Замените эти значения своими данными
TOKEN = "6564742799:AAHMDMyFj3uSo3-X3M9WukvsnBWyNY9TXfU"
ADMIN_ID = @sujessimi
SERVER_PUBLIC_KEY = "Wa3s9VB7CR58nPu5eI0UQ05HhpKhAm8035QvHJKdT0Q="
YOUR_SERVER_IP = "212.118.37.218"
YOUR_SERVER_PORT = "51830"

# Создание/подключение к базе данных
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Проверка и создание таблицы пользователей, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                 (name TEXT, speed TEXT, start_date TEXT, active BOOLEAN, telegram_username TEXT, role TEXT)''')
conn.commit()

def create_client_config(name, speed):
    # Это упрощенная версия. В реальной жизни, вы бы, вероятно, использовали wg-quick или другой инструмент.
    config = f"""
[Interface]
PrivateKey = CLIENT_PRIVATE_KEY
Address = 10.0.0.XX/24
DNS = 1.1.1.1

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {YOUR_SERVER_IP}:{YOUR_SERVER_PORT}
AllowedIPs = 0.0.0.0/0
    """
    # Замените CLIENT_PRIVATE_KEY и 10.0.0.XX соответствующими значениями
    return config

def restricted(func):
    """Decorator to restrict access to command to ADMIN only."""
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

@restricted
def start(update, context):
    """Handler for the /start command."""
    keyboard = [
        [InlineKeyboardButton("Create Client", callback_data='create_client')],
        [InlineKeyboardButton("List Clients", callback_data='list_clients')],
        [InlineKeyboardButton("Restart Server", callback_data='restart_server')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def create_client_callback(update, context):
    """Callback when admin chooses to create a client."""
    update.callback_query.message.reply_text("Please provide the client's name:")
    return "NAME"

def list_clients_callback(update, context):
    """Callback when admin chooses to list all clients."""
    # Fetch all clients from the database
    cursor.execute("SELECT * FROM users")
    clients = cursor.fetchall()
    if not clients:
        update.callback_query.message.reply_text("No clients found.")
        return

    for client in clients:
        client_info = f"Name: {client[0]}\nSpeed: {client[1]}\nStart Date: {client[2]}\nActive: {client[3]}"
        update.callback_query.message.reply_text(client_info)
    return

def restart_server_callback(update, context):
    """Callback when admin chooses to restart the server."""
    # Your server restart command here
    # For demonstration, I'm just printing
    print("Server restarted!")
    update.callback_query.message.reply_text("Server restarted!")

# Add more callback functions as per your needs

def main():
    """Main function to start the bot."""
    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher

    # Register the command handlers
    dp.add_handler(CommandHandler("start", start))

    # Register the callbacks
    dp.add_handler(CallbackQueryHandler(create_client_callback, pattern='create_client'))
    dp.add_handler(CallbackQueryHandler(list_clients_callback, pattern='list_clients'))
    dp.add_handler(CallbackQueryHandler(restart_server_callback, pattern='restart_server'))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
