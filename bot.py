import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = '6461780172:AAEABfAggnJDYVcFBsHQZJoFb-tNy2axaXY'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'keywords_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


class Keyword(Base):
    __tablename__ = 'keywords_keywords'

    id = Column(Integer, primary_key=True)
    keywords = Column(String, unique=True, nullable=False)
    message = Column(String)
    image_path = Column(String)


DATABASE_URL = "postgresql://bot:bot@localhost/admin_bot"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    # Save user data to the database
    session = SessionLocal()
    new_user = User(user_id=user.id, first_name=user.first_name, last_name=user.last_name, username=user.username)
    session.add(new_user)
    session.commit()
    session.close()

    await message.reply("Привет! Я бот. Отправь мне кодовое слово.")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    keyword = message.text

    session = SessionLocal()
    result = session.query(Keyword).filter_by(keywords=keyword).first()
    session.close()

    if result:
        response_message, image_path = result.message, result.image_path
        with open(image_path, 'rb') as photo:
            await message.reply_photo(photo, caption=response_message)
    else:
        await message.reply("Кодовое слово не найдено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
