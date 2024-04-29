import os
import openai
import asyncio
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from components.middleware import VoiceRateLimitMiddleware, InitMiddlewareFSM
from components.textmessage import get_answer_gpt
import aiofiles.os


# Загрузка переменных окуржения
load_dotenv()


# Загрузка ключа OpenAI
openai_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_key
openai.api_key = openai_key


# Создание роутера
router = Router()


# Настройка мидлварей
router.message.middleware(InitMiddlewareFSM())
router.message.middleware(VoiceRateLimitMiddleware(limit=2, window=60))


# Инициализация клиента OpenAI
client = OpenAI()


# Создаем ThreadPoolExecutor для запуска задач, по обработки голосвых сообщений, в отдельных потоках
executor = ThreadPoolExecutor(max_workers=3)


# Асинхронная функция обработки голосовых сообщений
async def transcribe_audio(avoice_file_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, transcribe_audio_sync, avoice_file_path)


# Синхронная функция выполнения транскрипции
def transcribe_audio_sync(svoice_file_path):
    with open(svoice_file_path, 'rb') as audio_file:
        transcription = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcription.text
    

# Обработчик аудиосообщений
@router.message(F.voice)
async def get_audio_translate(message: Message, state: FSMContext):
    
    voice_file_path = None

    try:
        # Уведомляем пользователя о том, что бот "печатает"
        await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        # Получаем расширение файла
        mime_types_file = message.voice.mime_type.split('/')

        # Создаём путь до аудиофайла
        voice_file_path = f"voice/{message.voice.file_id}{message.from_user.id}.{mime_types_file[-1]}"

        # Сохраняем аудио-сообщение
        await message.bot.download(message.voice.file_id, voice_file_path)

        # Запускаем транскрипцию в отдельном потоке
        transcription = await transcribe_audio(voice_file_path)

        # Вызываем обработчик для текстовых сообщений
        await get_answer_gpt(message, state, voice_text=transcription)

    finally:
        # Удаляем аудиофайл после обработки
        if voice_file_path and await aiofiles.os.path.exists(voice_file_path):
            await aiofiles.os.remove(voice_file_path)


# Код для отдельного запуска этого модуля
if __name__ == "__main__":
    pass