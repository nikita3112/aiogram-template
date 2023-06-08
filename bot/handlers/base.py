import logging

from aiogram import Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, CallbackQuery
from aiogram.utils.markdown import html_decoration as hd

from bot.dao.holder import HolderDao
from bot.models import dto
from bot.cbdata import CancelCallbackFactory


logger = logging.getLogger(__name__)

router = Router(name='base')

@router.message(CommandStart())
async def start_cmd(message: Message, user: dto.User):
    await message.reply(
        f'Привет, {message.from_user.first_name}!\n\n' \
        f'Я бот - менеджер канала с платной подпиской.'
    )

@router.callback_query(CancelCallbackFactory.filter())
async def cancel(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    return await state.clear()


def setup_base(dp: Dispatcher):
    dp.include_router(router)