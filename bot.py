from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаем подключение к базе данных с помощью SQLAlchemy
DATABASE_URL = "postgresql://bot:bot@localhost/admin_bot"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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


Base.metadata.create_all(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    # Сохранение данных пользователя в базе данных
    db_user = User(
        user_id=user.id, first_name=user.first_name,
        last_name=user.last_name,
        username=user.username)
    async with get_db() as db:
        db.add(db_user)
        db.commit()

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    async with get_db() as db:
        db_keyword = db.query(Keyword).filter(Keyword.keyword == keyword).first()

        if db_keyword:
            response_message, image_path = db_keyword.message, db_keyword.image_path
            with open(image_path, 'rb') as photo:
                await message.reply_photo(photo, caption=response_message)
        else:
            await message.reply("Кодовое слово не найдено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
