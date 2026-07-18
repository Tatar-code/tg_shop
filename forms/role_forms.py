from aiogram.fsm.state import State,StatesGroup

class AddAdminForm(StatesGroup):
    admin_tg_id = State()

class DelAdminForm(StatesGroup):
    admin_tg_id = State()