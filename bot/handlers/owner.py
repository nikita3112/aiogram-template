from asyncio import sleep

from aiogram import Dispatcher, Bot, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from sqlalchemy.exc import NoResultFound

from bot.models import dto
from bot.dao.holder import HolderDao
from bot.keyboards import get_owner_keyboard, get_cancel_keyboard, get_broadcast_edit_keyboard, get_broadcast_keyboard
from bot.filters.owner import OwnerFilter, OwnerCallbackFilter
from bot.cbdata import AddNewAdminCallbackFactory, DeleteAdminCallbackFactory, CreateBroadcastCallbackFactory, ConfirmBroadcastCallbackFactory, DeclineBroadcastCallbackFactory, AddBroadcastButtonCallbackFactory
from bot.states import AddNewAdminState, DeleteAdminState, Broadcast
from bot.services import broadcast


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
    message = await query.message.answer(
        text='Введите ID поьзователя',
        reply_markup=get_cancel_keyboard()
    )
    return await state.set_data({'message_id': message.message_id})

@router.message(AddNewAdminState.enter_user_id)
async def add_admin(message: Message, dao: HolderDao, user: dto.User, state: FSMContext, bot: Bot):
    data = await state.get_data()

    try:
        user_id = int(message.text)
    except ValueError:
        await state.clear()
        await bot.delete_message(message.from_user.id, data['message_id'])
        return await message.answer('Некорректный ID')
    
    try:
        user = await dao.user.get_by_tg_id(user_id)
    except NoResultFound:
        await state.clear()
        await bot.delete_message(message.from_user.id, data['message_id'])
        return await message.answer('Пользователь с таким ID не существует')
    
    if user.is_admin:
        await state.clear()
        await bot.delete_message(message.from_user.id, data['message_id'])
        return await message.answer('Пользователь уже админ')
    
    user = await dao.user.update_admin(user, True)
    await state.clear()
    await bot.delete_message(message.from_user.id, data['message_id'])
    return await message.answer('Админ успешно добавлен!')


# Delete admin
@router.callback_query(DeleteAdminCallbackFactory.filter())
async def delete_admin_callback(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(DeleteAdminState.enter_user_id)
    message = await query.message.answer(
        text='Введите ID поьзователя',
        reply_markup=get_cancel_keyboard()
    )
    return await state.set_data({'message_id': message.message_id})

@router.message(DeleteAdminState.enter_user_id)
async def add_admin(message: Message, dao: HolderDao, user: dto.User, state: FSMContext, bot: Bot):
    data = await state.get_data()

    try:
        user_id = int(message.text)
    except ValueError:
        await state.clear()
        await bot.delete_message(message.from_user.id, data['message_id'])
        return await message.answer('Некорректный ID')
    
    try:
        user = await dao.user.get_by_tg_id(user_id)
    except NoResultFound:
        await state.clear()
        await bot.delete_message(message.from_user.id, data['message_id'])
        return await message.answer('Пользователь с таким ID не существует')
    
    if not user.is_admin:
        await state.clear()
        await bot.delete_message(message.from_user.id, data['message_id'])
        return await message.answer('Пользователь не является админом')
    
    user = await dao.user.update_admin(user, False)
    await state.clear()
    await bot.delete_message(message.from_user.id, data['message_id'])
    return await message.answer('Админ успешно удален!')


# Broadcast
@router.callback_query(CreateBroadcastCallbackFactory.filter())
async def create_broadcast(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await state.set_state(Broadcast.send_broadcast_message)
    message = await query.message.answer(
        text='Отправьте сообщение для рассылки',
        reply_markup=get_cancel_keyboard()
    )
    return await state.set_data({'message_id': message.message_id})

@router.message(Broadcast.send_broadcast_message)
async def edit_broadcast(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.copy_message(
        chat_id=message.from_user.id,
        from_chat_id=message.from_user.id,
        message_id=message.message_id,
        reply_markup=get_broadcast_edit_keyboard()
    )
    await bot.delete_message(message.from_user.id, data['message_id'])
    await bot.delete_message(message.from_user.id, message.message_id)
    return await state.clear()

@router.callback_query(AddBroadcastButtonCallbackFactory.filter())
async def add_broadcast_button(query: CallbackQuery, state: FSMContext):
    await state.set_data({'copy_message_id': query.message.message_id})
    await state.set_state(Broadcast.enter_button_name)
    message = await query.message.answer(
        text='Введите текст кнопки',
        reply_markup=get_cancel_keyboard()
    )
    return await state.update_data({'message_id': message.message_id})

@router.message(Broadcast.enter_button_name)
async def enter_broadcast_button_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.delete_message(message.from_user.id, data['message_id'])
    await state.update_data({'button_name': message.text})
    await state.set_state(Broadcast.enter_button_url)
    message = await message.answer(
        text='Введите URL для кнопки',
        reply_markup=get_cancel_keyboard()
    )
    return await state.update_data({'message_id': message.message_id})

@router.message(Broadcast.enter_button_url)
async def enter_broadcast_button_url(message: Message, state: FSMContext, bot: Bot, dao: HolderDao):
    data = await state.get_data()

    await dao.broadcast_button.create(dto.BroadcastButton(name=data['button_name'], url=message.text))

    await bot.delete_message(message.from_user.id, data['message_id'])

    broadcast_buttons = await dao.broadcast_button.get_all()
    await bot.copy_message(
        chat_id=message.from_user.id,
        from_chat_id=message.from_user.id,
        message_id=data['copy_message_id'],
        reply_markup=get_broadcast_edit_keyboard(broadcast_buttons)
    )
    return await bot.delete_message(message.from_user.id, data['copy_message_id'])

@router.callback_query(ConfirmBroadcastCallbackFactory.filter())
async def confirm_broadcast(query: CallbackQuery, dao: HolderDao, bot: Bot):
    users = await dao.user.get_all()
    message = await query.message.answer(
        'Рассылка запущена'
    )

    broadcast_buttons = await dao.broadcast_button.get_all()
    count = await broadcast(
        bot=bot,
        users=users,
        from_chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=get_broadcast_keyboard(broadcast_buttons)
    )

    await message.delete()
    await dao.broadcast_button.delete_all()
    await query.message.delete()

    return await query.message.answer(
        'Рассылка окончена!\n' \
        f'Количество отправленных сообщений - {count}'
    )

@router.callback_query(DeclineBroadcastCallbackFactory.filter())
async def decline_broadcast(query: CallbackQuery, dao: HolderDao):
    await dao.broadcast_button.delete_all()
    return await query.message.delete()


def setup_owner(dp: Dispatcher):
    router.message.filter(OwnerFilter())
    router.callback_query.filter(OwnerCallbackFilter())
    dp.include_router(router)