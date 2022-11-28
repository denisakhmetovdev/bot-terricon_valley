from aiogram import types, Dispatcher

from conf.bot_creator import bot
from conf.sqlite_db import read_for_client
from keyboards.client_kb import kb_client


async def start_handler(msg: types.Message):
    try:
        await bot.send_message(msg.from_user.id, 'Приятных покупок', reply_markup=kb_client)
        await msg.delete()
    except:
        await msg.reply('Напишите боту:\nhttps://t.me/TerriconVExempleBot')


async def address_handler(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Складская 600 Офис 700')
    await msg.delete()


async def opened_handler(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Режим работы:\nс Пн по Пт с 9 до 19\nСб и Вс - выходной')
    await msg.delete()


async def goods_handler(msg: types.Message):
    await read_for_client(msg)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(address_handler, commands=['Расположение'])
    dp.register_message_handler(opened_handler, commands=['Режим_работы'])
    dp.register_message_handler(goods_handler, commands=['Товары'])
