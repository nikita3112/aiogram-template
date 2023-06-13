from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from bot.dao.holder import HolderDao
from bot.filters.admin import AdminFilter, AdminCallbackFilter


router = Router(name='admin')


@router.message(Command('stats', prefix='/'))
async def stats(message: Message, dao: HolderDao):
    count = await dao.user.get_active_users_count()
    return await message.answer(f'Актив за 24ч - {count}')

def setup_superuser(dp: Dispatcher):
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminCallbackFilter())
    dp.include_router(router)