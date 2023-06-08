from aiogram.filters.callback_data import CallbackData


class CancelCallbackFactory(CallbackData, prefix='cancel'):
    ...