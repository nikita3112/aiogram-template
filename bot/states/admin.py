from aiogram.fsm.state import StatesGroup, State


class AddNewAdminState(StatesGroup):
    enter_user_id = State()


class DeleteAdminState(StatesGroup):
    enter_user_id = State()