from aiogram.fsm.state import StatesGroup, State


class AddNewAdminState(StatesGroup):
    enter_user_id = State()


class DeleteAdminState(StatesGroup):
    enter_user_id = State()


class Broadcast(StatesGroup):
    send_broadcast_message = State()
    enter_button_name = State()
    enter_button_url = State()