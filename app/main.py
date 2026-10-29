import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Add it to your .env file.")

OWNER_ID = os.getenv("OWNER_ID")

dp = Dispatcher()

if OWNER_ID:
    OWNER_ID = int(OWNER_ID)
    dp.message.filter(F.from_user.id == OWNER_ID)
else:
    @dp.message.middleware()
    async def print_sender_id(handler, message: Message, data):
        logging.info("Telegram ID відправника: %s", message.from_user.id)
        return await handler(message, data)


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Привіт! Я допоможу тобі фіксувати твої витрати 💰")


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Я бот для фіксування витрат.\n\n"
        "Команди:\n"
        "/start — почати роботу з ботом\n"
        "/help — показати цей опис"
    )


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
