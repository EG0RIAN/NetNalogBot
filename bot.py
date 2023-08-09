import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def open_db():
    dsn = "postgresql://bot:bot@localhost/admin_bot"
    return await asyncpg.connect(dsn)


async def close_db(conn):
    await conn.close()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    # Сохранение данных пользователя в базе данных
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ""
    username = user.username

    conn = await open_db()
    await conn.execute(
        "INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES ($1, $2, $3, $4)",
        user.id, first_name, last_name, username)
    await conn.commit()
    await close_db(conn)

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    conn = await open_db()
    result = await conn.fetchrow(
        "SELECT message, image_path FROM keywords_keywords WHERE keywords=$1",
        keyword)
    await close_db(conn)

    if result:
        response_message, image_path = result
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Кодовое слово не найдено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
