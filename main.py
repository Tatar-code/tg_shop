from aiogram import Bot,Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

from os import getenv
from dotenv import load_dotenv
import asyncio

from database.db import set_pool,close_pool
from routers.urouter import user_router
from routers.arouter import admin_router
from routers.orouter import owner_router

load_dotenv()
dp = Dispatcher()
api_server = TelegramAPIServer.from_base(getenv('PROXY_URL').replace('/bot',''))
session = AiohttpSession(api=api_server)
bot = Bot(token=getenv('TOKEN'),session=session)


async def main():
    await set_pool(getenv('DSN'))
    print('БД подключена')
    
    dp.include_routers(user_router,admin_router,owner_router)
    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()
if __name__ == '__main__':
    asyncio.run(main())