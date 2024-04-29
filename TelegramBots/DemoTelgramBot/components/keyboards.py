from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура главного меню
mainKeyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    input_field_placeholder="Выберите команду",
    keyboard=[[KeyboardButton(text="Помощь")]])