from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime, timedelta


# Инициализация значений FSM
class InitMiddlewareFSM(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # Используем FSM для хранения данных
        state = data['state']
        
        # Инициализация списков
        list_history = []
        list_timestamps = []

        # Получаем данные FSMContext
        user_data = await state.get_data()

        # Инициализация переменных в FSMContext
        if not user_data:
            await state.update_data(history=list_history)
            await state.update_data(timestamps=list_timestamps)

        # Продолжаем обработку
        result = await handler(event, data)

        return result


# Общая настройка количества сообщений в минуту
class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, window: int = 60):
        self.limit = limit
        self.window = window

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        # Используем FSM для хранения данных
        state = data['state']
        
        # Получаем данные FSMContext
        user_data = await state.get_data()

        # Получаем временные метки из FSM
        timestamps = user_data.get("timestamps")

        # Получаем текущее временное значение        
        now = datetime.now()

        # Удаляем старые временные метки
        timestamps = [
            timestamp
            for timestamp in timestamps
            if now - timestamp < timedelta(seconds=self.window)
        ]

        # Проверяем, не превышен ли лимит
        if len(timestamps) >= self.limit:
            await event.reply("Пожалуйста, не отправляйте сообщения слишком часто.")
            return None

        # Добавляем текущую временную метку
        timestamps.append(now)

        # Сохраняем обновленные временные метки в FSM
        await state.update_data(timestamps=timestamps)

        # Продолжаем обработку
        result = await handler(event, data)

        return result