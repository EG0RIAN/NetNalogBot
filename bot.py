import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import asyncpg

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

DATABASE_URL = "postgresql://django:django@localhost/admin_bot"

# Create async connection pool for asyncpg
async def open_db():
    return await asyncpg.create_pool(DATABASE_URL)

async def close_db(pool):
    await pool.close()

Base = declarative_base()

class User(Base):
    __tablename__ = "keywords_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)

class Keyword(Base):
    __tablename__ = "keywords_keywords"

    keyword = Column(String, primary_key=True, index=True)
    message = Column(String)
    image_path = Column(String)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Handler functions


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    # Сохранение данных пользователя в базе данных (игнорируем дубликаты)
    db_user = User(user_id=user.id, first_name=user.first_name, last_name=user.last_name or "", username=user.username)
    pool = await open_db()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO keywords_users (user_id, first_name, last_name, username) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING",
            user.id, user.first_name, db_user.last_name, user.username)

    await message.reply("Привет! Я бот. Отправь мне ключевое слово.")

# Modify other handler functions similarly...

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
