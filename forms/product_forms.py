from aiogram.fsm.state import State,StatesGroup

class ProductForm(StatesGroup):
    photo_id = State()
    name = State()
    description = State()
    price = State()
    in_stock = State()
    category_name = State()

class CurrentCategoryForm(StatesGroup):
    category_name = State()

class CurrentProductForm(StatesGroup):
    all_product = State()
    current_product = State()
