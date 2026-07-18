from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.reply import owner_keyboard
from database.users_queries import create_user
from database.admins_queries import is_admin,is_owner,find_user_id_by_tg_id
from database.owners_queries import set_admin,del_admin
from database.product_queries import create_product,find_category_id_by_name
from forms.owner_forms import AddAdminForm,DelAdminForm,ProductForm

owner_router = Router()

def check_owner_acces(func):
    async def wrapper(message: Message,*args, **kwargs):
        if not await is_owner(tg_id=message.from_user.id):
            await message.answer('У вас нет доступа к этой функции')
            return 
        return await func(message, *args, **kwargs)
    return wrapper

@owner_router.message(Command('owner'))
@check_owner_acces
async def owner_menu(message: Message, **kwargs):
    if await is_owner(tg_id=message.from_user.id):
        await message.answer('Hello, creator',reply_markup=owner_keyboard)
    else:
        await message.answer('У вас нет прав для входа')

@owner_router.message(Command('stop'))
async def stop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ввод данных отключен')

@owner_router.message(F.text == 'Назначить администратора')
@check_owner_acces
async def add_admin(message: Message, state: FSMContext, **kwargs):
    await message.answer('Введите tg_id пользователя')
    await state.set_state(AddAdminForm.admin_tg_id)

@owner_router.message(AddAdminForm.admin_tg_id, F.text)
async def process_add_tg_id(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer('Введен неверный tg_id')
        return None
    
    user = await find_user_id_by_tg_id(tg_id=int(message.text))
    if user is None:
        await message.answer('Введен неверный tg_id')
        return None
    
    if await is_admin(tg_id=int(message.text)):
        await message.answer('Пользователь уже имеет админ права')
        return None
    await state.update_data(admin_tg_id=int(message.text))
    await set_admin(user_id=user)
    await message.answer(f'Админ права выданы пользователю {message.text}!')
    await state.clear()

@owner_router.message(F.text == 'Уволить администратора')
@check_owner_acces
async def stop_admin(message: Message, state: FSMContext, **kwargs):
    await message.answer('Введите tg_id администратора')
    await state.set_state(DelAdminForm.admin_tg_id)

@owner_router.message(DelAdminForm.admin_tg_id, F.text)
async def process_del_tg_id(message: Message, state: FSMContext):

    if not message.text.isdigit():
            await message.answer('Введен неверный tg_id')
            return None
    
    user = await find_user_id_by_tg_id(tg_id=int(message.text))
    if user is None:
        await message.answer('Введен неверный tg_id')
        return None

    
    if not await is_admin(tg_id=int(message.text)):
        await message.answer('Пользователь не является администратором')
        return None
    
    if await is_owner(tg_id=message.from_user.id):
        await message.answer('Владелец не может быть понижен')
        return None
    
    await state.update_data(admin_tg_id=int(message.text))
    await del_admin(user_id=user)
    await message.answer(f'Админ права сняты с пользователя {message.text}!')
    await state.clear()

@owner_router.message(F.text == 'Добавить товар')
@check_owner_acces
async def add_ProductForm(message: Message, state: FSMContext,**kwargs):
    await message.answer('Отправьте фотографию товара')
    await state.set_state(ProductForm.photo_id)

@owner_router.message(ProductForm.photo_id, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_id = photo.file_id
    await state.update_data(photo_id = photo_id)
    await message.answer('Введите название товара')
    await state.set_state(ProductForm.name)

@owner_router.message(ProductForm.name, F.text)
async def process_name(message: Message, state: FSMContext):
    if len(message.text) < 1 or len(message.text) > 100:
        await message.answer('Введите правильное название')
        return None
    
    await message.answer('Введите описание товара')
    await state.update_data(name=message.text)
    await state.set_state(ProductForm.description)

@owner_router.message(ProductForm.description, F.text)
async def process_description(message: Message, state: FSMContext):
    if len(message.text) < 10 or len(message.text) > 300:
        await message.answer('Введите правильное описание')
        return None
    
    await message.answer('Введите цену за товар')
    await state.update_data(description=message.text)
    await state.set_state(ProductForm.price)

@owner_router.message(ProductForm.price, F.text)
async def process_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введите числовое значение')
        return None
    if int(message.text) < 1 or int(message.text) > 1000000:
        await message.answer('Укажите цену в диапозоне от 1 до 1.000.000')
        return None 
    
    await message.answer('Введите количество товара в продаже')
    await state.update_data(price=message.text)
    await state.set_state(ProductForm.in_stock)

@owner_router.message(ProductForm.in_stock, F.text)
async def process_in_stock(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введите числовое значение')
        return None
    if int(message.text) < 0 or int(message.text) > 1000000:
        await message.answer('Укажите товары в диапозоне от 0 до 1.000.000')
        return None
    await state.update_data(in_stock=message.text)
    await message.answer('Введите категорию для товара')
    await state.set_state(ProductForm.category_name)

@owner_router.message(ProductForm.category_name, F.text)
async def process_category(message: Message, state: FSMContext):
    category = await find_category_id_by_name(category_name=message.text)
    if category is None:
        await message.answer('Введите существующую категорию')
        return None
    await state.update_data(category_name=message.text)
    data = await state.get_data()
    await create_product(name=data['name'],description=data['description'],price=int(data['price']),in_stock=int(data['in_stock']),category_id=category,photo_file_id=data['photo_id'])
    await message.answer('Товар добавлен')
    await state.clear()