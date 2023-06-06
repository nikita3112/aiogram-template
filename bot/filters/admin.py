from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.models import dto


class AdminFilter(BaseFilter):
    async def __call__(
            self,
            message: Message,
            user: dto.User
		) -> bool:
            return user.is_admin