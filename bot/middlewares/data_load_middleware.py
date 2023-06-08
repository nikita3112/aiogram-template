from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.dao.holder import HolderDao
from bot.models import dto


class LoadDataMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        holder_dao: HolderDao = data["dao"]
        data["user"] = await holder_dao.user.create_or_update_user(dto.User.from_aiogram(data["event_from_user"]))
        result = await handler(event, data)
        return result