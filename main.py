from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import subprocess
from io import BytesIO
import re

TOKEN = "6564742799:AAHMDMyFj3uSo3-X3M9WukvsnBWyNY9TXfU"
ADMIN_ID = 170663702
SERVER_PUBLIC_KEY = "Wa3s9VB7CR58nPu5eI0UQ05HhpKhAm8035QvHJKdT0Q="
YOUR_SERVER_IP = "212.118.37.218"
YOUR_SERVER_PORT = "51830"

def get_next_available_ip() -> str:
    with open('/etc/wireguard/wg0.conf', 'r') as f:
        contents = f.read()
    all_ips = re.findall(r"10.0.0.(\d+)", contents)
    if not all_ips:
        return "10.0.0.2"
    last_ip = max(int(ip) for ip in all_ips)
    return f"10.0.0.{last_ip + 1}"

def restricted(func):
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id != ADMIN_ID:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

@restricted
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Создать нового пользователя", callback_data='new_user'),
            InlineKeyboardButton("Перезагрузка сервера", callback_data='reboot_server'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_text('Выберите действие:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'new_user':
        private_key = subprocess.getoutput('wg genkey')
        public_key = subprocess.getoutput(f'echo {private_key} | wg pubkey')
        user_ip = get_next_available_ip()

        config = f"""[Interface]
PrivateKey = {private_key}
Address = {user_ip}/24
DNS = 8.8.8.8

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
AllowedIPs = 0.0.0.0/0
Endpoint = {YOUR_SERVER_IP}:{YOUR_SERVER_PORT}
"""

        with open('/etc/wireguard/wg0.conf', 'a') as f:
            f.write(config)

        bio = BytesIO()
        bio.name = 'vpn_config.conf'
        bio.write(config.encode())
        bio.seek(0)
        update.effective_message.reply_document(document=bio, filename='vpn_config.conf')

    elif query.data == 'reboot_server':
        subprocess.run(['sudo', 'reboot'])
        query.edit_message_text(text="Сервер перезагружается...")

def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

