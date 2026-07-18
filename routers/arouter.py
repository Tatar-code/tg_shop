from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from keyboards.reply import admin_keyboard
from database.admins_queries import is_admin,is_owner

admin_router = Router()

def check_admin_acces(func):
    async def wrapper(message: Message, *args):
        if not await is_admin(tg_id=message.from_user.id):
            await message.answer('У вас нет доступа к этой функции')
            return 
        return await func(message, *args)
    return wrapper

@admin_router.message(Command('admin'))
@check_admin_acces
async def admin_menu(message: Message):
        await message.answer('Вы успешно вошли в админ-панель',reply_markup=admin_keyboard)