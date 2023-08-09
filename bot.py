import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncpg
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Замените на свой токен
TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создание подключения к базе данных с помощью asyncpg
async def open_db():
    return await asyncpg.create_pool(database="admin_bot", user="bot", password="bot", host="localhost")

async def close_db(pool):
    await pool.close()

# SQLAlchemy
DATABASE_URL = "postgresql://django:django@localhost/admin_bot"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Keyword(Base):
    __tablename__ = "keywords_keywords"

    keyword = Column(String, primary_key=True, index=True)
    message = Column(String)
    image_path = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    return db

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    db = get_db()
    db_keyword = db.query(Keyword).filter(Keyword.keyword == keyword).first()

    if db_keyword:
        response_message, image_path = db_keyword.message, db_keyword.image_path
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Ключевое слово не найдено в базе данных.")

    db.close()

if __name__ == '__main__':
    asyncio.run(open_db())  # Открываем подключение к базе данных
    executor.start_polling(dp, skip_updates=True)
