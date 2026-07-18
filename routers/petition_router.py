from aiogram.types import Message,CallbackQuery

from aiogram import Router,F
from aiogram.fsm.context import FSMContext


from database.petition_queries import create_petition,get_data_by_petition
from keyboards.reply import support_keyboard,start_keyboard
from keyboards.inline import show_all_petitions_by_user
from forms.petition_forms import PetitionForm
from forms.filters import filter_length_text

petition_router = Router()

@petition_router.message(F.text == 'Техническая поддержка')
async def support(message: Message):
    await message.answer('Вы можете оставить обращение для нас',reply_markup=support_keyboard)


@petition_router.message(F.text == 'Написать обращение')
async def add_petition(message: Message, state: FSMContext):
    await message.answer('Напишите ваше обращение в чат')
    await state.set_state(PetitionForm.petition_text)

@petition_router.message(PetitionForm.petition_text, F.text)
async def process_petition(message: Message, state: FSMContext):
    filter_length = await filter_length_text(text=message.text, min=10, max=300)
    if filter_length is not None:
        await message.answer(filter_length)
        return None

    await state.update_data(petition_text=message.text)
    data=await state.get_data()
    await create_petition(tg_id=message.from_user.id, petition_text=data['petition_text'])
    await message.answer('Ваше обращение отправлено на рассмотрение',reply_markup=support_keyboard)
    await state.clear()

@petition_router.message(F.text == 'Мои обращения')
async def support(message: Message):
   keyboard = await show_all_petitions_by_user(tg_id=message.from_user.id)
   await message.answer('Ваши обращения',reply_markup=keyboard)


@petition_router.callback_query(F.data.startswith('petition_'))
async def show_data_by_petition(callback: CallbackQuery):
    petition_id = int(callback.data.split('_')[1])
    petition = await get_data_by_petition(petition_id=petition_id)
    await callback.message.edit_text(f'Обращение №{petition['petition_id']}\nТекст обращения: {petition['petition_text']}\nВремя обращения: {petition['created_at']}\nСостояние обращения: {'Закрыто' if petition['is_actual'] == False else 'В работе'}')
    await callback.answer()