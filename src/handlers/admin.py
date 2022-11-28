from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from conf.bot_creator import bot
from conf.sqlite_db import add_command, read_db, delete_from_db
from keyboards.admin_kb import admin_kb

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    title = State()
    description = State()
    price = State()


async def is_admin(msg: types.Message):
    global ID
    ID = msg.from_user.id
    await bot.send_message(msg.from_user.id, 'Права администратора получены', reply_markup=admin_kb)
    await msg.delete()


async def sm_start(msg: types.Message):
    await FSMAdmin.photo.set()
    await msg.reply('Загрузите фото')


async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply('Отменено')


async def load_photo(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = msg.photo[0].file_id
    await FSMAdmin.next()
    await msg.reply('Введите наименование товара')


async def load_title(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['title'] = msg.text
    await FSMAdmin.next()
    await msg.reply('Введите описание')


async def load_description(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
    await FSMAdmin.next()
    await msg.reply('Введите цену в тенге')


async def load_price(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['price'] = msg.text

    await add_command(state)
    await state.finish()
    await msg.answer('Сохранено в базу')


async def del_callback(callback_query: types.CallbackQuery):
    await delete_from_db(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалено', show_alert=True)


async def del_item(msg: types.Message):
    if msg.from_user.id == ID:
        read = await read_db()
        for ret in read:
            await bot.send_photo(msg.from_user.id, ret[0],  f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]} тенге')
            await bot.send_message(msg.from_user.id, text='^^^^^^^^^^^^^^^^^^^^^', reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton('Удалить', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(sm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['Отмена', 'отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_title, state=FSMAdmin.title)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(is_admin, commands=['isadmin'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback, Text(startswith='del '))
    dp.register_message_handler(del_item, commands=['Удалить'])
