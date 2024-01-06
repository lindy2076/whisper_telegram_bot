import logging
import asyncio
from os import makedirs
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode

from stt_bot.config import Config
from stt_bot.handlers import main_router


dp = Dispatcher()
settings = Config()


def get_app() -> Bot:
    token = settings.BOT_TOKEN
    if not token:
        logging.info("no token provided, exit")
        exit(1)
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
    return bot


async def main():
    bot = get_app()
    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    makedirs("tmp/", exist_ok=True)
    logging.basicConfig(
        format='%(levelname)s:%(asctime)s %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        filename='zlogz.log',
        level=logging.INFO
    )
    asyncio.run(main())
