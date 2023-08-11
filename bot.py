import os
import logging
import mysql.connector
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Configure logging
logging.basicConfig(level=logging.INFO)

# Your MySQL database credentials
DB_CONFIG = {
    'user': 'bot',
    'password': ')5+,h,X-J5FL',
    'host': 'localhost',
    'database': 'admin_bot',
}

# Initialize the bot and dispatcher
bot = Bot(token='6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Handlers
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or ' '
    last_name = message.from_user.last_name or ' '
    username = message.from_user.username or ' '
    
    # Create a connection to the MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # Check if the user is already in the database
        cursor.execute("SELECT user_id FROM keywords_users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            # Insert the user into the database
            cursor.execute("INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES (%s, %s, %s, %s)",
                        (user_id, first_name, last_name, username))
            conn.commit()
        
        await message.reply("Привет! Это бот!")
    finally:
        # Close the database connection
        cursor.close()
        conn.close()

@dp.message_handler(lambda message: not message.text.startswith('/'))
async def handle_keyword(message: types.Message):
    keyword = message.text
    
    # Create a connection to the MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Find the keyword in the database
        cursor.execute("SELECT * FROM keywords_keywords WHERE keyword = %s", (keyword,))
        result = cursor.fetchone()
        
        if result:
            keyword_id, _, response_message, image_path, file_path = result
            image_caption = response_message
            
            if image_path and image_path.strip() != '':
                image_path = os.path.join('admin_bot', 'media', image_path)
                if os.path.exists(image_path):
                    # Send a message with a photo if the image_path is provided
                    with open(image_path, 'rb') as photo:
                        await bot.send_photo(message.chat.id, photo, caption=image_caption)
            elif file_path and file_path.strip() != '':
                file_path = os.path.join('admin_bot', 'media', file_path)
                if os.path.exists(file_path):
                    # Send a message with a file if the file_path is provided
                    with open(file_path, 'rb') as file:
                        await bot.send_document(message.chat.id, file, caption=image_caption)
            else:
                # Send a message without a photo or file
                await message.reply(image_caption)
        else:
            await message.reply("Ключевое слово не найдено.")
    finally:
        # Close the database connection
        cursor.close()
        conn.close()

# Start the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
