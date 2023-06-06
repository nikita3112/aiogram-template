from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.middlewares.config_middleware import ConfigMiddleware
from bot.middlewares.data_load_middleware import LoadDataMiddleware
from bot.middlewares.db_middleware import DBMiddleware
from bot.models.config.main import BotConfig


def setup_middlewares(dp: Dispatcher, pool: async_sessionmaker[AsyncSession], bot_config: BotConfig):
    dp.update.outer_middleware(ConfigMiddleware(bot_config))
    dp.update.outer_middleware(DBMiddleware(pool))
    dp.update.outer_middleware(LoadDataMiddleware())