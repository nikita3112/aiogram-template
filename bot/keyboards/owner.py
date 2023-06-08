from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import AddNewAdminCallbackFactory, DeleteAdminCallbackFactory


def get_owner_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
				text='Добавить админа',
                callback_data=AddNewAdminCallbackFactory().pack()
			)
        ],
        [
            InlineKeyboardButton(
                text='Удалить админа',
                callback_data=DeleteAdminCallbackFactory().pack()
            )
        ]
	]
    return InlineKeyboardMarkup(inline_keyboard=buttons)