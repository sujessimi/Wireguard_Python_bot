import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id

    if user_id == :
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = KeyboardButton("Создать нового клиента")
        item2 = KeyboardButton("Перезагрузка сервера")
        markup.add(item1, item2)

        await message.answer("Выберите действие:", reply_markup=markup)
    else:
        await message.answer("У вас нет доступа к этим функциям.")

@dp.message_handler(lambda message: message.text == "Создать нового клиента")
async def create_client(message: types.Message):
    # TODO: Добавьте код для создания нового клиента
    await message.answer("Клиент создан!")

@dp.message_handler(lambda message: message.text == "Перезагрузка сервера")
async def reboot_server(message: types.Message):
    # TODO: Добавьте код для перезагрузки сервера
    await message.answer("Сервер перезагружается!")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

