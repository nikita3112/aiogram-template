from aiogram.filters.callback_data import CallbackData


class AddNewAdminCallbackFactory(CallbackData, prefix='add_admin'):
    ...