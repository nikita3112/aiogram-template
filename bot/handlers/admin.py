from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.models import dto
from bot.dao.holder import HolderDao
from bot.filters.admin import AdminFilter, AdminCallbackFilter
from bot.keyboards import get_owner_keyboard
from bot.cbdata import AddNewAdminCallbackFactory
from bot.states import AddNewAdminState
from bot.services.user import update_user


router = Router(name='admin')


@router.message(Command('stats', prefix='/'))
async def stats(message: Message, dao: HolderDao):
    count = await dao.user.get_active_users_count()
    print(count)

    return await message.answer(f'Актив за 24ч - {count}')

@router.message(Command('owner', prefix='/'))
async def owner(message: Message):
    return await message.answer(
        text = f'Меню владельца',
        reply_markup=get_owner_keyboard()
    )

@router.callback_query(AddNewAdminCallbackFactory.filter())
async def add_admin_callback(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(AddNewAdminState.enter_user_id)
    return await query.message.answer('Введите ID поьзователя')

@router.message(AddNewAdminState.enter_user_id)
async def add_admin(message: Message, dao: HolderDao, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        return await message.answer('Некорректный ID')
    
    user = await dao.user.get_by_tg_id(user_id)

    if not user:
        return await message.answer('Пользователь с таким ID не существует')
    
    if user.is_admin:
        return await message.answer('Пользователь уже админ')
    
    user.is_admin = True


    user = await update_user(user, dao.user)
    await state.clear()

    return await message.answer('Админ успешно добавлен!')

def setup_superuser(dp: Dispatcher):
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminCallbackFilter())
    dp.include_router(router)