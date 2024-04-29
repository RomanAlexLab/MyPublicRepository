from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import components.keyboards as kb


# Создание роутера
router = Router()


# Обработчик команды: /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=kb.mainKeyboard)


# Обработчик сообщения: Помощь
@router.message(F.text == 'Помощь')
async def help_me(message: Message):
    await message.answer(f"Кнопка Помощь - помощь\nКоманда /start - запуск бота")