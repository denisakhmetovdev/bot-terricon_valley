from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


load_btn = KeyboardButton('/Загрузить')
del_btn = KeyboardButton('/Удалить')

admin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(load_btn).add(del_btn)
