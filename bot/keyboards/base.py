from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import CancelCallbackFactory


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
				text='Отмена',
                callback_data=CancelCallbackFactory().pack()
			)
        ]
	]
    return InlineKeyboardMarkup(inline_keyboard=buttons)