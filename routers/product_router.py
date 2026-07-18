from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.user_queries import get_user_by_tg_id
from database.product_queries import get_category_id_by_name,create_product,get_all_products_by_category_name
from database.cart_queries import create_cart, add_product_to_cart,get_cart_by_tg_id
from keyboards.reply import show_all_categories,start_keyboard,catalog_keyboard,keyboard_without_last_product,keyboard_without_next_product
from forms.product_forms import ProductForm,CurrentCategoryForm,CurrentProductForm
from forms.filters import filter_length_text,filter_only_number
from routers.role_router import check_owner_acces


product_router = Router()


@product_router.message(F.text == 'Добавить товар')
@check_owner_acces
async def add_product(message: Message, state: FSMContext,**kwargs):
    await message.answer('Отправьте фотографию товара')
    await state.set_state(ProductForm.photo_id)

@product_router.message(ProductForm.photo_id, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_id = photo.file_id
    await state.update_data(photo_id = photo_id)
    await message.answer('Введите название товара')
    await state.set_state(ProductForm.name)

@product_router.message(ProductForm.name, F.text)
async def process_name(message: Message, state: FSMContext):
    length = await filter_length_text(text=message.text, min=5, max=100)
    if length is not None:
        await message.answer(text=length)
        return None
    
    await message.answer('Введите описание товара')
    await state.update_data(name=message.text)
    await state.set_state(ProductForm.description)

@product_router.message(ProductForm.description, F.text)
async def process_description(message: Message, state: FSMContext):
    length_filter = await filter_length_text(text=message.text, min=10, max=300)
    if length_filter is not None:
        await message.answer(text=length_filter)
        return None
    
    await message.answer('Введите цену за товар')
    await state.update_data(description=message.text)
    await state.set_state(ProductForm.price)

@product_router.message(ProductForm.price, F.text)
async def process_price(message: Message, state: FSMContext):
    number_filter = await filter_only_number(text=message.text)
    if number_filter is not None:
        await message.answer(text=number_filter)
        return None
    if int(message.text) < 1 or int(message.text) > 1000000:
        await message.answer('Укажите цену в диапозоне от 1 до 1.000.000')
        return None 
    
    await message.answer('Введите количество товара в продаже')
    await state.update_data(price=message.text)
    await state.set_state(ProductForm.in_stock)

@product_router.message(ProductForm.in_stock, F.text)
async def process_in_stock(message: Message, state: FSMContext):
    number_filter = await filter_only_number(text=message.text)
    if number_filter is not None:
        await message.answer(text=number_filter)
        return None
    if int(message.text) < 0 or int(message.text) > 1000000:
        await message.answer('Укажите количество товаров в диапозоне от 0 до 1.000.000')
        return None
    
    await state.update_data(in_stock=message.text)
    await message.answer('Введите категорию для товара')
    await state.set_state(ProductForm.category_name)

@product_router.message(ProductForm.category_name, F.text)
async def process_category(message: Message, state: FSMContext):

    category = await get_category_id_by_name(category_name=message.text)
    if category is None:
        await message.answer('Введите существующую категорию')
        return None
    await state.update_data(category_name=message.text)
    data = await state.get_data()
    await create_product(name=data['name'],description=data['description'],price=int(data['price']),in_stock=int(data['in_stock']),category_id=category,photo_file_id=data['photo_id'])
    await message.answer('Товар добавлен')
    await state.clear()

@product_router.message(F.text == 'Каталог')
async def catalog(message: Message,state: FSMContext):
    await message.answer('Выберите категорию товара',reply_markup=await show_all_categories())
    await state.set_state(CurrentCategoryForm.category_name)

@product_router.message(CurrentCategoryForm.category_name, F.text)
async def process_category(message: Message, state: FSMContext):
    category = await get_category_id_by_name(category_name=str(message.text))
    if category is None:
        await message.answer('Такой категории не существует')
        return None
    all_product = await get_all_products_by_category_name(category_name=message.text)
    first_product = all_product[0]
    await state.update_data(category_name = message.text)
    await message.answer_photo(photo=first_product['photo_file_id'],caption=f'{first_product['name']}\n{first_product['price']}р\n{first_product['description']}\n{first_product['reviews']}',reply_markup=catalog_keyboard)
    await state.clear()
    await state.set_state(CurrentProductForm.all_product)
    await state.update_data(all_product = all_product)
    await state.set_state(CurrentProductForm.current_product)
    await state.update_data(current_product = 1)

@product_router.message(F.text == 'Следующий')
async def next_product(message: Message, state: FSMContext):
    data = await state.get_data()
    all_product = data['all_product']
    current_product = data['current_product']
    if current_product < len(all_product) - 1:
        product = all_product[current_product]
        await message.answer_photo(photo=product['photo_file_id'],caption=f'{product['name']}\n{product['price']}р\n{product['description']}\n{product['reviews']}')
        await state.set_state(CurrentProductForm.current_product)
        await state.update_data(current_product = current_product + 1)

    if current_product == len(all_product) - 1:
        product = all_product[current_product]
        await message.answer_photo(photo=product['photo_file_id'],caption=f'{product['name']}\n{product['price']}р\n{product['description']}\n{product['reviews']}',reply_markup=keyboard_without_next_product)
        await state.set_state(CurrentProductForm.current_product)
        await state.update_data(current_product = current_product)
    
@product_router.message(F.text == 'Назад')
async def last_product(message: Message, state: FSMContext):
    data = await state.get_data()
    all_product = data['all_product']
    current_product = data['current_product']
    last_product = current_product - 1
    if last_product > 0:
        product = all_product[last_product]
        await message.answer_photo(photo=product['photo_file_id'],caption=f'{product['name']}\n{product['price']}р\n{product['description']}\n{product['reviews']}')
        await state.set_state(CurrentProductForm.current_product)
        await state.update_data(current_product = last_product)
    
    if last_product == 0:
        product = all_product[last_product]
        await message.answer_photo(photo=product['photo_file_id'],caption=f'{product['name']}\n{product['price']}р\n{product['description']}\n{product['reviews']}',reply_markup=keyboard_without_last_product)
        await state.set_state(CurrentProductForm.current_product)
        await state.update_data(current_product = last_product + 1)
    else:
        await message.answer(text='Ошибка',reply_markup=start_keyboard)
        await state.clear()

@product_router.message(F.text == 'В корзину')
async def to_cart(message: Message,state: FSMContext):
    data = await state.get_data()
    cart = await get_cart_by_tg_id(tg_id=message.from_user.id)
    current_product = data['current_product']
    all_product = data['all_product']
    product_id = all_product[current_product - 1]
    await add_product_to_cart(cart_id=cart['cart_id'], product_id=product_id['product_id'])
    await message.answer('Товар добавлен в корзину')
