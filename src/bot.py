from aiogram.utils import executor
from conf.bot_creator import dp
from handlers.client import register_handlers_client
from handlers.admin import register_handlers_admin
from conf.sqlite_db import sqlite_db


async def startup(_):
    print('Бот онлайн')
    sqlite_db()


register_handlers_client(dp)
register_handlers_admin(dp)


executor.start_polling(dp, skip_updates=True, on_startup=startup)
