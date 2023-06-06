from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.dao.holder import HolderDao
from bot.models import dto
from bot.services.user import create_or_update_user


class LoadDataMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        holder_dao = data["dao"]
        data["user"] = await save_user(data, holder_dao)
        result = await handler(event, data)
        return result


async def save_user(data: dict[str, Any], holder_dao: HolderDao) -> dto.User:
    return await create_or_update_user(
        dto.User.from_aiogram(data["event_from_user"]),
        holder_dao.user
    )