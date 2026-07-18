from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.users_queries import all_petitions_by_user

btn1 = InlineKeyboardButton(text='Назад',callback_data='back_product')
btn2 = InlineKeyboardButton(text='В корзину', callback_data='to_cart')
btn3 = InlineKeyboardButton(text='Следующий',callback_data='next_product')
keyboard_in_catalog = InlineKeyboardMarkup(inline_keyboard=[
    [btn1,btn3],
    [btn2]])

async def show_all_petitions_by_user(tg_id: int):
    
    builder = InlineKeyboardBuilder()

    for petition in await all_petitions_by_user(tg_id=tg_id):
        builder.button(text=f'Обращение №{petition}', callback_data=f'petition_{petition}')
    
    builder.adjust(1)
    return builder.as_markup()
