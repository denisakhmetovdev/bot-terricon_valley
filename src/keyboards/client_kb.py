from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


button1 = KeyboardButton('/Расположение')
button2 = KeyboardButton('/Режим_работы')
button3 = KeyboardButton('/Товары')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(button1, button2).add(button3)
