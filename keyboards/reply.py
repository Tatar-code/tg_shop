from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.product_queries import get_all_categories,get_all_products_by_category_name


btn1 = KeyboardButton(text='Каталог')
btn2 = KeyboardButton(text='Корзина')
btn3 = KeyboardButton(text='Профиль')
btn4 = KeyboardButton(text='Техническая поддержка')

btn5 = KeyboardButton(text='Обращения')
btn6 = KeyboardButton(text='Заказы')

btn7 = KeyboardButton(text='Добавить товар')
btn8 = KeyboardButton(text='Назначить администратора')
btn9 = KeyboardButton(text='Уволить администратора')

btn10 = KeyboardButton(text='Написать обращение')
btn11 = KeyboardButton(text='Мои обращения')
btn12 = KeyboardButton(text='Назад')

btn13 = KeyboardButton(text='Назад')
btn14 = KeyboardButton(text='Следующий')
btn15 = KeyboardButton(text='В корзину')


start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn1,btn2],
    [btn3,btn4]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn5],
    [btn6]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')

owner_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn7],
    [btn8,btn9]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')

support_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn10],
    [btn11],
    [btn12]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')

catalog_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn13,btn14],
    [btn15]],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие')

async def show_all_categories():
    builder = ReplyKeyboardBuilder()

    for category in await get_all_categories():
        builder.button(text=category['category_name'])
        
    builder.adjust(2)
    
    return builder.as_markup(resize_keyboard=True)

# async def show_all_products_by_category(category_name: str):
#     builder = ReplyKeyboardBuilder()

#     for product in await get_all_products_by_category_name(category_name=category_name):
#         builder.button(text=product['name'])
    
#         builder.adjust(2)

#     return builder.as_markup(resize_keyboard=True)