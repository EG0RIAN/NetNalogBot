import logging
import mysql.connector
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Your Telegram Bot API token
API_TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'

# Your MySQL database configuration
DB_CONFIG = {
    'user': 'bot',
    'password': ')5+,h,X-J5FL',
    'host': 'localhost',
    'database': 'admin_bot',
}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db_connection = mysql.connector.connect(**DB_CONFIG)
db_cursor = db_connection.cursor()

# Handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    # Check if the user already exists in the database
    db_cursor.execute("SELECT * FROM keywords_users WHERE user_id = %s", (user_id,))
    user_exists = db_cursor.fetchone()

    if not user_exists:
        # Insert the user into the database
        db_cursor.execute(
            "INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES (%s, %s, %s, %s)",
            (user_id, first_name, last_name or '', username)
        )
        db_connection.commit()

    await message.answer("Привет! Это бот!")

# Handler for any other text message
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    keyword = message.text.strip()

    # Check if the keyword exists in the database
    db_cursor.execute("SELECT * FROM keywords_keywords WHERE keyword = %s", (keyword,))
    keyword_data = db_cursor.fetchone()

    if keyword_data:
        _, _, response_message, image_path = keyword_data
        with open(image_path, 'rb') as photo:
            await message.answer_photo(photo, caption=response_message)
    else:
        await message.answer("Keyword not found.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
