from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.exc import NoResultFound

from bot.models import dto
from bot.dao.holder import HolderDao
from bot.keyboards import get_owner_keyboard, get_cancel_keyboard
from bot.filters.owner import OwnerFilter, OwnerCallbackFilter
from bot.cbdata import AddNewAdminCallbackFactory, DeleteAdminCallbackFactory
from bot.states import AddNewAdminState, DeleteAdminState


router = Router(name='owner')


@router.message(Command('owner', prefix='/'))
async def owner(message: Message):
    return await message.answer(
        text=f'Меню владельца',
        reply_markup=get_owner_keyboard()
    )


# Add new admin
@router.callback_query(AddNewAdminCallbackFactory.filter())
async def add_admin_callback(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(AddNewAdminState.enter_user_id)
    return await query.message.answer(
        text='Введите ID поьзователя',
        reply_markup=get_cancel_keyboard()
    )

@router.message(AddNewAdminState.enter_user_id)
async def add_admin(message: Message, dao: HolderDao, user: dto.User, state: FSMContext):
    try:
        user_id = int(message.text)
    except ValueError:
        return await message.answer('Некорректный ID')
    
    try:
        user = await dao.user.get_by_tg_id(user_id)
    except NoResultFound:
        return await message.answer('Пользователь с таким ID не существует')
    
    if user.is_admin:
        await state.clear()
        return await message.answer('Пользователь уже админ')
    
    user = await dao.user.update_admin(user, True)
    await state.clear()
    return await message.answer('Админ успешно добавлен!')


# Delete admin
@router.callback_query(DeleteAdminCallbackFactory.filter())
async def delete_admin_callback(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(DeleteAdminState.enter_user_id)
    return await query.message.answer(
        text='Введите ID поьзователя',
        reply_markup=get_cancel_keyboard()
    )

def setup_owner(dp: Dispatcher):
    router.message.filter(OwnerFilter())
    router.callback_query.filter(OwnerCallbackFilter())
    dp.include_router(router)