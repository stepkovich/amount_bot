import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
import asyncio
from aiogram.filters import Command
from get_data import get_info_async

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


def start():
    print('Bot starting')


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Введите артикул:")


@dp.message(F.text)
async def get_article(message: types.Message):
    article = message.text.upper()
    api_answer = await get_info_async(article)
    await message.answer(api_answer)



@dp.message()
async def err(message: types.Message):
    await message.answer("Хммм, на артикул не похоже")


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    start()
    asyncio.run(main())
