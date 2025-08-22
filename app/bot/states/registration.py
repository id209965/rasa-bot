from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    phone = State()
    first_name = State()
    last_name = State()
    gender = State()
    age = State()
    region = State()
    interests = State()
    photo = State()
    location = State()
    confirm = State()
