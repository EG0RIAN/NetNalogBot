import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
conn = sqlite3.connect('admin_bot/db.sqlite3')
cursor = conn.cursor()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    # Сохранение данных пользователя в базу данных
    first_name = user.first_name
    last_name = user.last_name if user.last_name else "" 
    username = user.username

    cursor.execute(
        "INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                (user.id, first_name, last_name, username))
    conn.commit()

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    # Поиск сообщения и пути к изображению по ключевому слову в базе данных
    cursor.execute(
        "SELECT message, image_path FROM keywords_keywords WHERE keywords=?",
        (keyword,))
    result = cursor.fetchone()

    if result:
        response_message, image_path = result
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Кодовое слово не найдено.")

executor.start_polling(dp, skip_updates=True)
