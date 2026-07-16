from aiogram.fsm.state import State,StatesGroup

class AddAdmin(StatesGroup):
    admin_tg_id = State()

class DelAdmin(StatesGroup):
    admin_tg_id = State()

class Product(StatesGroup):
    name = State()
    description = State()
    price = State()
    in_stock = State()