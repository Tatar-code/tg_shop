from aiogram.types import Message,CallbackQuery,InputMediaPhoto
from aiogram.filters import CommandStart,Command
from aiogram import Router,F
from aiogram.fsm.context import FSMContext

import asyncio

from keyboards.reply import start_keyboard,support_keyboard,show_all_categories,catalog_keyboard
from keyboards.inline import show_all_petitions_by_user
from database.users_queries import create_user,create_petition,get_data_by_petition
from database.admins_queries import is_admin,is_owner,find_user_id_by_tg_id,find_user_data_by_id
from database.product_queries import find_category_id_by_name,get_all_products_by_category_name,send_product_to_cart
from forms.user_forms import PetitionForm,FindCategoryForm,CurrentProductForm

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text=f'Добро пожаловать, {message.from_user.full_name}',reply_markup=start_keyboard), await create_user(tg_id=message.from_user.id, username=message.from_user.username)

@user_router.message(Command('stop'))
async def stop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ввод данных отключен')

@user_router.message(F.text == 'Техническая поддержка')
async def support(message: Message):
    await message.answer('Вы можете оставить обращение для нас',reply_markup=support_keyboard)

# @user_router.message(F.text == 'Назад')
# async def back_from_support(message: Message):
#     await message.answer('Вы вернулись в главное меню',reply_markup=start_keyboard)


@user_router.message(F.text == 'Написать обращение')
async def add_petition(message: Message, state: FSMContext):
    await message.answer('Напишите ваше обращение в чат')
    await state.set_state(PetitionForm.petition_text)

@user_router.message(PetitionForm.petition_text, F.text)
async def process_petition(message: Message, state: FSMContext):
    if message.text != 'Назад':
        await state.update_data(petition_text=message.text)
        data=await state.get_data()
        await create_petition(tg_id=message.from_user.id, petition_text=data['petition_text'])
        await message.answer('Ваше обращение отправлено на рассмотрение')
        await state.clear()
    else:
        await message.answer('Вы вернулись в главное меню',reply_markup=start_keyboard)
        await state.clear()

@user_router.message(F.text == 'Мои обращения')
async def support(message: Message):
   keyboard = await show_all_petitions_by_user(tg_id=message.from_user.id)
   await message.answer('Ваши обращения',reply_markup=keyboard)

@user_router.message(F.text == 'Каталог')
async def catalog(message: Message,state: FSMContext):
    await message.answer('Выберите категорию товара',reply_markup=await show_all_categories())
    await state.set_state(FindCategoryForm.category_name)

@user_router.message(FindCategoryForm.category_name, F.text)
async def process_category(message: Message, state: FSMContext):
    category = await find_category_id_by_name(category_name=str(message.text))
    if category is None:
        await message.answer('Такой категории не существует')
        return None
    global current_category
    current_category = message.text
    all_product = await get_all_products_by_category_name(category_name=message.text)
    first_product = all_product[0]
    await state.update_data(category_name = message.text)
    await message.answer_photo(photo=first_product['photo_file_id'],caption=f'{first_product['name']}\n{first_product['price']}р\n{first_product['description']}\n{first_product['reviews']}',reply_markup=catalog_keyboard)
    await state.clear()
    await state.set_state(CurrentProductForm.all_product)
    await state.update_data(all_product = all_product)
    await state.set_state(CurrentProductForm.current_product)
    await state.update_data(current_product = 1)

@user_router.message(F.text == 'Следующий')
async def next_product(message: Message, state: FSMContext):
    next_product = 1
    data = await state.get_data()
    current_product = data['current_product']
    if next_product <= current_product:
        all_product = data['all_product']
        product = all_product[current_product]
        next_product += 1
        await message.answer_photo(photo=product['photo_file_id'],caption=f'{product['name']}\n{product['price']}р\n{product['description']}\n{product['reviews']}')
        await state.set_state(CurrentProductForm.current_product)
        await state.update_data(current_product = next_product)
    else:
        await message.answer(text='Товары закончились',reply_markup=start_keyboard)
        await state.clear()
    
@user_router.message(F.text == 'Назад')
async def last_product(message: Message, state: FSMContext):
    data = await state.get_data()
    all_product = data['all_product']
    current_product = data['current_product']
    last_product = current_product - 1
    if last_product >= 1:
        product = all_product[last_product]
        await message.answer_photo(photo=product['photo_file_id'],caption=f'{product['name']}\n{product['price']}р\n{product['description']}\n{product['reviews']}')
        await state.set_state(CurrentProductForm.current_product)
        await state.update_data(current_product = last_product)
    else:
        await message.answer(text='Хорош заебал',reply_markup=start_keyboard)
        await state.clear()

@user_router.message(F.text == 'В корзину')
async def to_cart(message: Message,state: FSMContext):
    data = await state.get_data()
    user_id = await find_user_id_by_tg_id(tg_id=message.from_user.id)
    user = await find_user_data_by_id(user_id=user_id)
    cart_id = user['user_cart']
    current_product = data['current_product']
    all_product = data['all_product']
    product_id = all_product[current_product - 1]
    await send_product_to_cart(cart_id=cart_id, product_id=product_id['product_id'])
    await message.answer('Товар добавлен в корзину')



@user_router.callback_query(F.data.startswith('petition_'))
async def give_data_by_petition(callback: CallbackQuery):
    petition_id = int(callback.data.split('_')[1])
    petition = await get_data_by_petition(petition_id=petition_id)
    await callback.message.edit_text(f'Обращение №{petition['petition_id']}\nТекст обращения: {petition['petition_text']}\nВремя обращения: {petition['created_at']}\nСостояние обращения: {'Закрыто' if petition['is_actual'] == False else 'В работе'}')
    await callback.answer()