from aiogram import BaseMiddleware
from typing import Callable, Any, Awaitable

from aiogram.types import TelegramObject

from bot.models.config.main import Config


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config):
        self.config = config

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        return await handler(event, data)