data = {
    'dispatcher': <Dispatcher '0x7a5239f6eeb0'>,
    'bots': (<aiogram.client.bot.Bot object at 0x7a5239f6eeb0>,),
    'bot': <aiogram.client.bot.Bot object at 0x7a5239f6eeb0>,
    'event_from_user': User(
        id=0000000000,
        is_bot=False,
        first_name='Роман',
        last_name=None,
        username='Roman',
        language_code='ru'
    ),
    'event_chat': Chat(
        id=0000000000,
        type='private',
        first_name='Роман',
        username='Roman'
    ),
    'fsm_storage': <aiogram.fsm.storage.memory.MemoryStorage object at 0x7a5239f6eeb0>,
    'state': <aiogram.fsm.context.FSMContext object at 0x7a5239f6eeb0>,
    'handler': HandlerObject(
        callback=<function get_answer_gpt at 0x7a5239f6eeb0>,
        awaitable=True
    ),
    'event_update': Update(
        update_id=0000000000,
        message=Message(
            message_id=0000,
            date=datetime.datetime(2024, 4, 27, 9, 23, 35),
            chat=Chat(
                id=0000000000,
                type='private',
                first_name='Роман',
                username='Roman'
            ),
            from_user=User(
                id=0000000000,
                first_name='Роман',
                username='Roman'
            ),
            text='Привет'
        )
    ),
    'event_router': <Router '0x7a5239f6eeb0'>
}