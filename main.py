from aiogram.utils import executor
from config import dp
import logging
import asyncio

from handlers import client, callback, extra, fsmAdminMenu, admin, notification
from database.bot_dp import sql_create


async def on_startup(_):
    asyncio.create_task(notification.scheduler())
    sql_create()


admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
fsmAdminMenu.register_handlers_fsmmenu(dp)
notification.register_handler_notification(dp)

extra.register_handlers_extra(dp)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
