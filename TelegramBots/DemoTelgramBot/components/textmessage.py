import os
import openai
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from aiogram import F, Router
from aiogram.types import Message
from aiogram.enums import ChatAction
from components.middleware import RateLimitMiddleware, InitMiddlewareFSM
from aiogram.fsm.context import FSMContext
from config import SYSTEM_PROMT, USER_INPUT, MEMORY_MESSAGES, MODEL_GPT


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
router.message.middleware(RateLimitMiddleware(limit=3, window=60))


# Загрузка векторного хранилища
embeddings = OpenAIEmbeddings()
database  = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)


# Создание ретривера
retriever=database.as_retriever(search_kwargs={"k": 2, "score_threshold": 0.5})


# Инициализация модели
model = ChatOpenAI(model=MODEL_GPT)


# Обработчик
@router.message(F.text)
async def get_answer_gpt(message: Message, state: FSMContext, voice_text=None):

    # Уведомляем пользователя о том, что бот "печатает"
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Сохраняем текст сообщения в переменную
    if voice_text == None:
        text_message = message.text
    else:    
        text_message = voice_text

    # Получаем данные FSMContext
    data = await state.get_data()

    # Получаем историю сообщений
    HISTORY = data.get("history")
    
    # Добавляем сообщение в историю
    HISTORY.append(HumanMessage(content=text_message))

    # Формируем шаблон промпта
    template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(SYSTEM_PROMT),
            *HISTORY,
            HumanMessagePromptTemplate.from_template(USER_INPUT),
        ]
    )

    # Выполняем поиск по индексной базе
    chanks = await retriever.ainvoke(HISTORY[-1].content)

    # Формируем контекст
    search_context = ' '
    for i in range(len(chanks)):
        search_context = search_context + ' ' + chanks[i].page_content

    # Формируем промпт
    messages = template.format_messages(user_name=message.from_user.full_name, context=search_context, user_input=HISTORY[-1].content)

    # Выполняем запрос
    result = await model.ainvoke(messages)
    
    # Добавляем ответ в историю
    HISTORY.append(AIMessage(content=result.content))

    # Обновляем историю
    if len(HISTORY) >= MEMORY_MESSAGES:
        HISTORY = HISTORY[-MEMORY_MESSAGES:]
    
    # Обновляем данные FSMContext
    await state.update_data(history=HISTORY)

    # Получаем новые данные FSMContext и печатаем в CLI
    help_data = await state.get_data()

    # Печатаем в CLI
    print("Данные в обработчике:", help_data)

    # Отправляем ответ в чат
    await message.reply(HISTORY[-1].content)


# Код для отдельного запуска этого модуля
if __name__ == "__main__":
    pass