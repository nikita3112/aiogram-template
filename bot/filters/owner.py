from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.models import dto
from bot.models.config.main import Config


class OwnerFilter(BaseFilter):
    async def __call__(
            self,
            message: Message,
            config: Config
		) -> bool:
            return message.from_user.id == config.owner
    

class OwnerCallbackFilter(BaseFilter):
    async def __call__(
            self,
            query: CallbackQuery,
            config: Config
		) -> bool:
            return query.from_user.id == config.owner