

import random
import sqlite3
from config import bot


def sql_create():
    global dp, cursor
    dp = sqlite3.connect('bot.sqlite3')
    cursor = dp.cursor()

    if dp:
        print("база данных подключена!")


    dp.execute("CREATE TABLE IF NOT EXISTS menu"
               "(name TEXT PRIMARY KEY, username TEXT,"
               "photo TEXT, description TEXT,"
               "price INTEGER)")
    dp.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO menu VALUES"
                       "(?, ?, ?, ?, ?)", tuple(data.values()))
        dp.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM menu").fetchall()
    random_user = random.choice(result)

    await bot.send_photo(message.from_user.id, random_user[2],
                         caption=f"Name: {random_user[3]}\n"
                                 f"Description: {random_user[4]}\n"
                                 f"Price: {random_user[5]}\n\n"
                                 f"{random_user[1]}")


async def sql_command_all():
    return cursor.execute("SELECT * FROM menu").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM menu WHERE id == ?", (id,))
    dp.commit()


async def sql_commands_get_all_id():
    return cursor.execute('SELECT id FROM menu').fetchall()