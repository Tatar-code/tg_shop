from aiogram import Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message

from keyboards.reply import start_keyboard
from database.user_queries import create_user
registration_router = Router()

@registration_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f'Добро пожаловать, {message.from_user.full_name}',reply_markup=start_keyboard)
    await create_user(tg_id=message.from_user.id, username=message.from_user.username)

