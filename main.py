import asyncio
from datetime import datetime, timedelta
from pyrogram import Client
from pyrogram.types import Message
from loguru import logger
from pyrogram.handlers import MessageHandler
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker
from sqlalchemy.sql import select
import sqlalchemy.orm


PATH_TO_IMG = 'img_for_bot/rim-temple-of-sighs1-s.jpg'

Base = sqlalchemy.orm.declarative_base()
engine = create_async_engine('postgresql+asyncpg://testuser:test1234@localhost/UsersDB')
async_session = async_sessionmaker(engine, expire_on_commit=False)

API_ID = 21359826
API_HASH = 'acc4a0412485fc46d3e5679f2c2b25ec'
SESSION_NAME = 'FunnelBotTest'
CHANNEL_USERNAME = 'SashaGavrilin'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


async def on_message(message: Message):
    logger.info(f'Received message: {message.text}')
    if message.text == '/users_today':  # Command to view the number of registered people in the database for today.
        await get_users_today(message.chat.id)
    else:
        await on_message(message)


# Automatically send messages to the user.
async def on_message(app, message: Message):
    async with async_session() as session:
        user = await session.execute(select(User).filter_by(id=message.from_user.id))
        user = user.scalar_one_or_none()
        if not user:
            user = User(id=message.from_user.id)
            session.add(user)
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
    async with async_session(engine) as session:
        today = datetime.utcnow().date()
        count = session.query(User).filter(User.created_at >= today).count()
        await app.send_message(chat_id, f"Количество зарегистрированных пользователей сегодня: {count}")


if __name__ == '__main__':
    app.add_handler(MessageHandler(on_message))
    app.run()
