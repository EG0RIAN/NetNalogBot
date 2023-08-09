import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'
DATABASE_URL = 'postgresql://bot:bot@localhost/admin_bot'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def setup_database():
    return await asyncpg.create_pool(DATABASE_URL)


async def insert_user(pool, user):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES ($1, $2, $3, $4)",
            user.id, user.first_name, user.last_name or '', user.username
        )


async def get_response_and_image(pool, keyword):
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            "SELECT message, image_path FROM keywords_keywords WHERE keywords=$1",
            keyword
        )
        return result


async def on_start(message: types.Message):
    user = message.from_user
    pool = message.bot.get('db_pool')

    await insert_user(pool, user)

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")


async def handle_message(message: types.Message):
    keyword = message.text
    pool = message.bot.get('db_pool')

    result = await get_response_and_image(pool, keyword)

    if result:
        response_message, image_path = result
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Кодовое слово не найдено.")


async def on_startup(dp):
    await bot.send_message(chat_id=739247122, text="Бот запущен")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(setup_database())

    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(
        handle_message, content_types=types.ContentTypes.TEXT)

    executor.start_polling(dp, skip_updates=True)
