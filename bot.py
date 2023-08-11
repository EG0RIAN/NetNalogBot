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

# Handler for any text message
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    keyword = message.text.strip()

    # Check if the keyword exists in the database
    db_cursor.execute("SELECT * FROM keywords_keywords WHERE keyword = %s", (keyword,))
    keyword_data = db_cursor.fetchone()

    if keyword_data:
        _, _, response_message, image_path = keyword_data
        with open(image_path, 'rb') as photo:
            caption = response_message if response_message else None
            await message.answer_photo(photo, caption=caption)
    else:
        await message.answer("Keyword not found.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
