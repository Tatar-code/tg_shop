from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database.role_queries import is_owner,is_admin,set_admin,del_admin
from database.user_queries import get_user_by_tg_id
from keyboards.reply import admin_keyboard,owner_keyboard
from forms.role_forms import AddAdminForm,DelAdminForm
from forms.filters import filter_only_number

role_router = Router()

def check_owner_acces(func):
    async def wrapper(message: Message,*args, **kwargs):
        if not await is_owner(tg_id=message.from_user.id):
            await message.answer('У вас нет доступа к этой функции')
            return 
        return await func(message, *args, **kwargs)
    return wrapper

def check_admin_acces(func):
    async def wrapper(message: Message, *args):
        if not await is_admin(tg_id=message.from_user.id):
            await message.answer('У вас нет доступа к этой функции')
            return 
        return await func(message, *args)
    return wrapper

@role_router.message(Command('owner'))
@check_owner_acces
async def owner_menu(message: Message, **kwargs):
    if await is_owner(tg_id=message.from_user.id):
        await message.answer('Вы вошли в панель владельца',reply_markup=owner_keyboard)
    else:
        await message.answer('У вас нет прав для входа')

@role_router.message(Command('stop'))
async def stop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ввод данных отключен')


@role_router.message(F.text == 'Назначить администратора')
@check_owner_acces
async def add_admin(message: Message, state: FSMContext, **kwargs):
    await message.answer('Введите tg_id пользователя')
    await state.set_state(AddAdminForm.admin_tg_id)

@role_router.message(AddAdminForm.admin_tg_id, F.text)
async def process_add_tg_id(message: Message, state: FSMContext):

    number_filter = await filter_only_number(text=message.text)
    if number_filter is not None:
        await message.answer(text=number_filter)
        return None
    
    user = await get_user_by_tg_id(tg_id=int(message.text))
    if user is None:
        await message.answer('Пользователя с таким tg_id не существует')
        return None
    
    if await is_admin(tg_id=int(message.text)):
        await message.answer('Пользователь уже имеет админ права')
        return None
    
    await state.update_data(admin_tg_id=int(message.text))
    await set_admin(user_id=user['user_id'])
    await message.answer(f'Админ права выданы пользователю ({user['username']})!')
    await state.clear()

@role_router.message(F.text == 'Уволить администратора')
@check_owner_acces
async def stop_admin(message: Message, state: FSMContext, **kwargs):
    await message.answer('Введите tg_id администратора')
    await state.set_state(DelAdminForm.admin_tg_id)

@role_router.message(DelAdminForm.admin_tg_id, F.text)
async def process_del_tg_id(message: Message, state: FSMContext):

    number_filter = await filter_only_number(text=message.text)
    if number_filter is not None:
        await message.answer(text=number_filter)
        return None
    
    user = await get_user_by_tg_id(tg_id=int(message.text))
    if user is None:
        await message.answer('Пользователя с таким tg_id не существует')
        return None
    
    if not await is_admin(tg_id=int(message.text)):
        await message.answer('Пользователь не является администратором')
        return None
    
    if await is_owner(tg_id=int(message.text)):
        await message.answer('Владелец не может быть понижен')
        return None
    
    await state.update_data(admin_tg_id=int(message.text))
    await del_admin(user_id=user['user_id'])
    await message.answer(f'Админ права сняты с пользователя ({user['username']})!')
    await state.clear()

@role_router.message(Command('admin'))
@check_admin_acces
async def admin_menu(message: Message):
        await message.answer('Вы успешно вошли в админ-панель',reply_markup=admin_keyboard)
