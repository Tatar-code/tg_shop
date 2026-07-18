from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.petition_queries import get_all_petitions_by_tg_id

async def show_all_petitions_by_user(tg_id: int):
    
    builder = InlineKeyboardBuilder()

    for petition in await get_all_petitions_by_tg_id(tg_id=tg_id):
        builder.button(text=f'Обращение №{petition['petition_id']}', callback_data=f'petition_{petition['petition_id']}')
    
    builder.adjust(1)
    return builder.as_markup()
