from aiogram.filters.callback_data import CallbackData


class AddNewAdminCallbackFactory(CallbackData, prefix='add_admin'):
    ...


class DeleteAdminCallbackFactory(CallbackData, prefix='delete_admin'):
    ...


class CreateBroadcastCallbackFactory(CallbackData, prefix='broadcast'):
    ...


class ConfirmBroadcastCallbackFactory(CallbackData, prefix='confirm_broadcast'):
    ...


class DeclineBroadcastCallbackFactory(CallbackData, prefix='decline_broadcast'):
    ...


class AddBroadcastButtonCallbackFactory(CallbackData, prefix='add_broadcast_button'):
    ...