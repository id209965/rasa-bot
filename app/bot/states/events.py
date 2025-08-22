from aiogram.fsm.state import State, StatesGroup


class EventCreationStates(StatesGroup):
    title = State()
    date = State()
    time = State()
    interests = State()
    address = State()
    description = State()
    image = State()
    invite_friends = State()
    confirm = State()


class EventSearchStates(StatesGroup):
    search_criteria = State()
    region = State()
    interest = State()
    date_range = State()
