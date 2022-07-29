from aiogram import types, Dispatcher
from config import ADMIN, bot
from database.bot_dp import sql_commands_get_all_id


async def reklama(message: types.Message):
    if message.from_user.id in ADMIN:
        result = await sql_commands_get_all_id()
        for id in result:
            await bot.send_message(id[0], message.text[3::])

    else:
        await message.answer('ты не админ')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(reklama, commands=['R'])
