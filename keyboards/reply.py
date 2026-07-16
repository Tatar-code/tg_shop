from aiogram.types import KeyboardButton,InlineKeyboardButton,ReplyKeyboardMarkup,InlineKeyboardMarkup


btn1 = KeyboardButton(text='Профиль')
btn2 = KeyboardButton(text='Корзина')
btn3 = KeyboardButton(text='Техническая поддержка')
btn4 = KeyboardButton(text='Отзывы')

btn5 = KeyboardButton(text='Обращения')
btn6 = KeyboardButton(text='Заказы')

btn7 = KeyboardButton(text='Добавить товар')
btn8 = KeyboardButton(text='Назначить администратора')
btn9 = KeyboardButton(text='Уволить администратора')
start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn1,btn2],
    [btn3,btn4]],
    resize_keyboard=True,
    input_field_placeholder='Выберите поле')


admin_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn5],
    [btn6]],
    resize_keyboard=True,
    input_field_placeholder='Выберите поле')

owner_keyboard = ReplyKeyboardMarkup(keyboard=[
    [btn7],
    [btn8,btn9]],
    resize_keyboard=True,
    input_field_placeholder='Выберите поле')