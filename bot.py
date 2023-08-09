from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

DATABASE_URL = "postgresql://django:django@localhost/admin_bot"
engine = create_async_engine(DATABASE_URL, echo=True)  # Используем create_async_engine для асинхронной работы

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

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        async with session.begin():
            yield session

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    async with get_db() as db:
        db_user = User(user_id=user.id, first_name=user.first_name, last_name=user.last_name, username=user.username)
        db.add(db_user)
        await db.commit()

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    async with get_db() as db:
        db_keyword = await db.execute(Keyword.__table__.select().where(Keyword.keyword == keyword))
        db_keyword = await db_keyword.scalar_one_or_none()

    if db_keyword:
        response_message, image_path = db_keyword.message, db_keyword.image_path
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Кодовое слово не найдено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
