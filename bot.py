import mysql.connector
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Replace with your MySQL database connection details
db_config = {
    'user': 'bot',
    'password': ')5+,h,X-J5FL',
    'host': 'localhost',
    'database': 'admin_bot',
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    # Save user data to the MySQL database
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ""
    username = user.username

    cursor.execute(
        "INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES (%s, %s, %s, %s)",
        (user.id, first_name, last_name, username))
    conn.commit()

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    # Search for the message and image path using the keyword in the MySQL database
    cursor.execute(
        "SELECT message, image_path FROM keywords_keywords WHERE keywords=%s",
        (keyword,))
    result = cursor.fetchone()

    if result:
        response_message, image_path = result
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Кодовое слово не найдено.")


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
