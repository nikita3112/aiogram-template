from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.cbdata import AddNewAdminCallbackFactory, DeleteAdminCallbackFactory, CreateBroadcastCallbackFactory, ConfirmBroadcastCallbackFactory, DeclineBroadcastCallbackFactory, AddBroadcastButtonCallbackFactory, CancelCallbackFactory


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
        ],
        [
            InlineKeyboardButton(
                text='Создать рассылку',
                callback_data=CreateBroadcastCallbackFactory().pack()
            )
        ]
	]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_broadcast_keyboard(broadcast_buttons: list | None = None) -> InlineKeyboardMarkup:
    if broadcast_buttons:
        buttons = [
            [
                InlineKeyboardButton(
                    text=button.name,
                    url=button.url
                )
            ]
            for button in broadcast_buttons
        ]
    else:
        buttons = []
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_broadcast_edit_keyboard(broadcast_buttons: list | None = None) -> InlineKeyboardMarkup:
    if broadcast_buttons:
        buttons = [
            [
                InlineKeyboardButton(
                    text=button.name,
                    url=button.url
                )
            ]
            for button in broadcast_buttons
        ]
    else:
        buttons = []

    buttons.extend([
        [
            InlineKeyboardButton(
                text='✅',
                callback_data=ConfirmBroadcastCallbackFactory().pack()
            ),
            InlineKeyboardButton(
				text='❌',
                callback_data=DeclineBroadcastCallbackFactory().pack()
			)
        ],
        [
            InlineKeyboardButton(
                text='Добавить кнопку-ссылку',
                callback_data=AddBroadcastButtonCallbackFactory().pack()
            )
        ],
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)