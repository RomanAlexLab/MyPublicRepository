from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import components.keyboards as kb


# Создание роутера
router = Router()


# Обработчик команды: /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n\nЭто демонстрационный Телеграм-бот, призванный продемонстрировать мои технические навыки.\n\nМеня зовут Роман, и я являюсь разработчиком данного бота. Мой Telegram: @Roman89n.\n\nЭтот бот был написан на aiogram за несколько дней.\n\nСсылка на код бота: https://github.com/RomanAlexLab/MyPublicRepository/tree/main/TelegramBots/DemoTelgramBot\n\nБот является асинхронным, поддерживает текстовые сообщения и аудиосообщения.\n\nОбработка аудиосообщений вынесена в отдельный пул потоков, так как их обработка не является асинхронной.\n\nВ боте предусморена система памяти с использованием состояний FSM, а также система логирования\n\nВ боте использован фреймворк LangChain и API OpenAI.\n\nТакже в боте предусмотрено промежуточное программное обеспечение, которое контролирует количество запросов пользователей в минуту.\n\nБот слегка обучен на базе знаний, но поскольку это демонстрационный вариант, я не сильно беспокоился о качестве ответов.\n\nДля вас это означает, что вы можете увидеть, как работает практически необученная модель на начальном этапе.\n\nЧтобы убедиться, что модель обучена на вашей базе, задавайте простые вопросы, которые содержат конкретику, например: Что такое АРО?.\n\nПо всем возникающим вопросам обращайтесь.", reply_markup=kb.mainKeyboard)


# Обработчик сообщения: Помощь
@router.message(F.text == 'Помощь')
async def help_me(message: Message):
    await message.answer(f"Команда: /start - запуск бота\n\nКоманда: Помощь - вызов справки\n\nТекстовое сообщение - задать вопрос модели GPT\n\nАудосообщение - задать вопрос модели GPT")