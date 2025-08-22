from aiogram.fsm.state import State, StatesGroup


class ProfileEditStates(StatesGroup):
    edit_name = State()
    edit_age = State()
    edit_gender = State()
    edit_region = State()
    edit_interests = State()
    edit_photo = State()
    edit_location = State()
