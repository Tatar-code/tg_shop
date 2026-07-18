from aiogram.fsm.state import State,StatesGroup

class PetitionForm(StatesGroup):
    petition_text = State()
