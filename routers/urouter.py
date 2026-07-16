from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from aiogram import Router

from keyboards.reply import start_keyboard
from database.users import create_user
from database.admins import is_admin,is_owner

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f'Добро пожаловать, {message.from_user.full_name}',reply_markup=start_keyboard), await create_user(tg_id=message.from_user.id, username=message.from_user.username)