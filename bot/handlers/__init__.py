import logging

from aiogram import Dispatcher

from bot.handlers.base import setup_base
from bot.handlers.errors import setup_errors
from bot.handlers.admin import setup_superuser
from bot.models.config.main import BotConfig

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, bot_config: BotConfig):
    setup_errors(dp, bot_config.log_chat)
    setup_superuser(dp)
    setup_base(dp)
    logger.debug("handlers configured successfully")