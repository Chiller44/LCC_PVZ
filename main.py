import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from handlers import base_info, temperature, heat_exchanger, airflow, components, filters
from status import Addtinal_components
from handlers import start




BOT_TOKEN = os.getenv("TGBT")
#print("BOT_TOKEN from env:", repr(BOT_TOKEN))
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(base_info.router)
dp.include_router(temperature.router)
dp.include_router(heat_exchanger.router)
dp.include_router(airflow.router)
dp.include_router(components.router)
dp.include_router(filters.router)
dp.include_router(start.router)



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())