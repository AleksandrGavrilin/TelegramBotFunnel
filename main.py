import asyncio
from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.types import Message
from loguru import logger
from pyrogram.handlers import MessageHandler
from sqlalchemy import Column, Integer, DateTime, func, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker
from sqlalchemy.sql import select
import sqlalchemy.orm


PATH_TO_IMG = 'img_for_bot/rim-temple-of-sighs1-s.jpg'

Base = sqlalchemy.orm.declarative_base()
engine = create_async_engine('postgresql+asyncpg://testuser:test1234@localhost/UsersDB')
async_session = async_sessionmaker(engine, expire_on_commit=False)

API_ID = 00000000
API_HASH = ''
SESSION_NAME = ''
CHANNEL_USERNAME = ''


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)


app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Command processing.
async def on_message(app, message: Message):
    await init_models()
    logger.info(f'Received message: {message.text}')
    if message.text == '/users_today':  # Command to view the number of registered people in the database for today.
        await get_users_today(message.chat.id)
    else:
        await bot_message(app, message)


# Automatically send messages to the user.
async def bot_message(app, message: Message):
    async with async_session() as session:
        user = await session.execute(select(User).filter_by(id=message.from_user.id))
        user = user.scalar_one_or_none()
        if not user:
            user = User(id=message.from_user.id)
            session.add(user)
            await session.commit()
            await session.flush()
            await app.send_message(message.chat.id, 'Добрый день!')
            await asyncio.sleep(5400)  # sending message after 90 minutes
            await app.send_message(message.chat.id, 'Подготовила для вас материал')
            await asyncio.sleep(1)  # sending photo
            await app.send_photo(message.chat.id, PATH_TO_IMG)
            await asyncio.sleep(7200)  # sending message after 2 hours
            if not await check_trigger():
                await app.send_message(message.chat.id, 'Скоро вернусь с новым материалом!')


async def check_trigger():
    async for message in app.search_messages(CHANNEL_USERNAME, query='Хорошего дня'):
        if (datetime.utcnow() - message.date) < timedelta(minutes=10):
            return True
        return False


# Function to request the number of people registered today.
async def get_users_today(chat_id):
    async with async_session() as session:
        today = datetime.utcnow().date()
        result = await session.execute(select(func.count(User.id)).filter(User.created_at >= today))
        await app.send_message(chat_id, f"Количество зарегистрированных пользователей сегодня: {result.scalar_one()}")


if __name__ == '__main__':
    app.add_handler(MessageHandler(on_message))
    app.run()
