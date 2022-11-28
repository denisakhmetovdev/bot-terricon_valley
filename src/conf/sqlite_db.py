import sqlite3 as sq
from .bot_creator import bot


base = sq.connect('store.db')
cur = base.cursor()


def sqlite_db():
    if base:
        print('Подключение к базе данных - OK')
    base.execute('CREATE TABLE IF NOT EXISTS goods(photo TEXT, title TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO goods VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def read_for_client(msg):
    for ret in cur.execute('SELECT * FROM goods').fetchall():
        await bot.send_photo(msg.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена: {ret[3]} тенге')


async def read_db():
    return cur.execute('SELECT * FROM goods').fetchall()


async def delete_from_db(data):
    cur.execute('DELETE FROM goods WHERE title == ?', (data,))
