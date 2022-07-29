from aiogram import types, Dispatcher
from config import bot, ADMIN
import random


# @dp.message_handler()
async def echo(message: types.Message):
    if message.text.startswith('game'):
        if message.chat.type != 'private':
            if message.from_user.id in ADMIN:
                emg = ['🎯', '🎳', '🏀', '🎰', '🎲', '⚽']
                r_emg = random.choice(emg)
                await bot.send_dice(message.chat.id, emoji=r_emg)

            else:
                await message.answer('ты не повелитель!!!!!!!')

        else:
            await message.answer('это работает только в чатах')
    else:
        try:
            k = int(message.text)
            await bot.send_message(message.chat.id, k * k)
        except:
            await message.reply(message.text)


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
