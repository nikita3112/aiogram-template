from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from functools import partial

from bot.models import dto
from bot.filters.admin import AdminFilter


router = Router(name='admin')


@router.message(Command('admin', prefix='/'))
async def test(message: Message, user: dto.User):
    return await message.reply('U ARE ADMIN!')


def setup_superuser(dp: Dispatcher):
    router.message.filter(AdminFilter())
    dp.include_router(router)