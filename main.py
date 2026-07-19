from aiogram import Bot,Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

import os
from dotenv import load_dotenv
import asyncio

from database.db import set_pool,close_pool
from routers.petition_router import petition_router
from routers.product_router import product_router
from routers.role_router import role_router
from routers.registation_router import registration_router
load_dotenv()
dp = Dispatcher()
api_server = TelegramAPIServer.from_base(os.getenv('PROXY_URL').replace('/bot',''))
session = AiohttpSession(api=api_server)
bot = Bot(token=os.getenv('TOKEN'),session=session)


async def main():
    load_dotenv()
    await set_pool(dsn=os.getenv('DSN'))
    print('БД подключена')
    
    dp.include_routers(petition_router,product_router,role_router,registration_router)
    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()
if __name__ == '__main__':
    asyncio.run(main())