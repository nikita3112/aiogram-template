from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import AddNewAdminCallbackFactory


def get_owner_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
				text='Добавить админа',
                callback_data=AddNewAdminCallbackFactory().pack()
			)
        ]
	]
    return InlineKeyboardMarkup(inline_keyboard=buttons)