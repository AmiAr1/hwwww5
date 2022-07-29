import asyncio
import aioschedule
from aiogram import types, Dispatcher
from config import bot



async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text="ok")


async def go_to():
    await bot.send_message(chat_id=chat_id, text='помой машину')


async def work():
    photo = open("media/milashka.jpg", "rb")
    await bot.send_photo(chat_id=chat_id, photo=photo, caption="пора практиковаться!")


async def scheduler():
    aioschedule.every().monday.at("18:30").do(go_to)
    aioschedule.every().day.at("14:30").do(work)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3)


def register_handler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'напомни' in word.text)
