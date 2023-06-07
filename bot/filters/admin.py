from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.models import dto
from bot.models.config.main import Config


class AdminFilter(BaseFilter):
    async def __call__(
            self,
            message: Message,
            user: dto.User,
            config: Config
		) -> bool:
            return user.is_admin | message.from_user.id == config.owner
    

class AdminCallbackFilter(BaseFilter):
    async def __call__(
            self,
            query: CallbackQuery,
            user: dto.User,
            config: Config
		) -> bool:
            return user.is_admin | query.from_user.id == config.owner