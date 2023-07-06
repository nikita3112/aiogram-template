import logging
import os
from pathlib import Path

from aiogram import Dispatcher, Bot
from sqlalchemy.orm import close_all_sessions

from bot.config import load_config
from bot.config.logging_config import setup_logging
from bot.handlers import setup_handlers
from bot.middlewares import setup_middlewares
from bot.models.config.main import Paths
from bot.models.db import create_pool
from bot.schedulers.base import setup_scheduler


logger = logging.getLogger(__name__)


async def main():
    paths = get_paths()

    setup_logging(paths)
    config = load_config(paths)

    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML"
    )

    dp = Dispatcher(storage=config.storage.create_storage(), bot=bot)

    scheduler = setup_scheduler(bot, config, paths)
    dp['scheduler'] = scheduler

    setup_middlewares(dp, create_pool(config.db), config)
    setup_handlers(dp, config.bot)

    logger.info("started")
    try:
        scheduler.start()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        close_all_sessions()
        logger.info("stopped")


def get_paths() -> Paths:
    if path := os.getenv("BOT_PATH"):
        return Paths(Path(path))
    return Paths(Path(__file__).parent.parent)


if __name__ == '__main__':
    main()