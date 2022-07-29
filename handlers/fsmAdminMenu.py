from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import bot_dp

from config import bot, ADMIN


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        if message.from_user.id in ADMIN:
            try:
                await FSMAdmin.photo.set()
                await message.answer(f"Hi {message.from_user.full_name} "
                                     f"\nотправь фото блюда..")
            except:
                await message.answer('ЧЕЛ, ПРОСИЛИ ФОТО!')
        else:
            await message.answer('ты не повелитель!!!!!!!')
    else:
        await message.reply("пищи в личку!!")


async def photo_dish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data["username"] = f"@{message.from_user.username}"
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer('добавь название блюда')


async def name_dish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('добавь описание блюда')


async def description_dish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer('добавь цену')


async def price_dish(message: types.Message, state: FSMContext):

    try:
        if int(message.text) <= 0:
            await message.answer('НЕ НУ ЧЕЛ, ТК 99% МОИ, ДАЮ ШАНС ПОДУМАТЬ ЕЩЕ!')
        else:
            async with state.proxy() as data:
                data['price'] = int(message.text)
                await bot.send_photo(message.from_user.id, data['photo'],
                                     caption=f"Name: {data['name']}\n"
                                             f"Description: {data['description']}\n"
                                             f"Price: {data['price']}\n\n"
                                             f"{data['username']}")

            await bot_dp.sql_command_insert(state)
            await state.finish()
            await message.answer('Благодарю, теперь у нас присутствует это блюдо')
    except:
        await message.answer('ЦЕНУ ЦИФРАМИ УКАЗЫВАЮТ.')




async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer('Регистрация отменена!')


async def delete_data(message: types.Message):
    if message.from_user.id in ADMIN and message.chat.type == "private":
        users = await bot_dp.sql_command_all()
        for user in users:
            await bot.send_photo(message.from_user.id, user[2],
                                 caption=f"Name: {user[3]}\n"
                                         f"Description: {user[4]}\n"
                                         f"Price: {user[5]}\n\n"
                                         f"{user[1]}",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"delete: {user[3]}",
                                         callback_data=f"delete {user[0]}"
                                     )
                                 )
                                 )
    else:
        await message.reply("ты не админ!")


async def complete_delete(call: types.CallbackQuery):
    await bot_dp.sql_command_delete(call.data.replace('delete', ''))
    await call.answer(text='пользователь удален', show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_fsmmenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands='cancel')
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state="*")

    dp.register_message_handler(fsm_start, commands=['menu'])
    dp.register_message_handler(photo_dish, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(name_dish, state=FSMAdmin.name)
    dp.register_message_handler(description_dish, state=FSMAdmin.description)
    dp.register_message_handler(price_dish, state=FSMAdmin.price)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith('delete')
    )
