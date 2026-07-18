from aiogram.fsm.state import State,StatesGroup
from aiogram.types import Message

class AddAdminForm(StatesGroup):
    admin_tg_id = State()

class DelAdminForm(StatesGroup):
    admin_tg_id = State()

class ProductForm(StatesGroup):
    photo_id = State()
    name = State()
    description = State()
    price = State()
    in_stock = State()
    category_name = State()
