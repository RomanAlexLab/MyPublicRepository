import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from components.handlers import router as router_command
from components.gpt import router as gpt_router
from components.audiomessage import router as audio_router


# Загрузка переменных окуржения
load_dotenv()


# Загрузка токена Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')


# Настройка логгирования в файл. Уровень INFO / WARNING
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger()
handler = logging.FileHandler(filename='bot.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# Инициализация бота
bot = Bot(token=TOKEN)


# Инициализация диспетчера
dp = Dispatcher()


# Основной цикл
async def main():
    dp.include_router(router_command)
    dp.include_router(gpt_router)
    dp.include_router(audio_router)
    await dp.start_polling(bot)


# Запуск программы (Основного цикла) 
if __name__ == "__main__":
    asyncio.run(main())
