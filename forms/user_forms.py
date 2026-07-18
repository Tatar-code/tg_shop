from aiogram.fsm.state import State,StatesGroup

class PetitionForm(StatesGroup):
    petition_text = State()

class FindCategoryForm(StatesGroup):
    category_name = State()

class CurrentProductForm(StatesGroup):
    all_product = State()
    current_product = State()
