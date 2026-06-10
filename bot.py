import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
import asyncio
from aiogram.filters import Command
from get_data import get_info_async

load_dotenv()

TOKEN = os.getenv("TOKEN")
print(f"=== ОТЛАДКА: Длина токена: {len(TOKEN) if TOKEN else 0} ===")
print(f"=== ОТЛАДКА: Сам токен: [{TOKEN}] ==//=")

bot = Bot(token=TOKEN)
dp = Dispatcher()


def start():
    print('Bot starting')


@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Введите артикул:")


# Ловим только текст, который не начинается с /
@dp.message(F.text)
async def get_article(message: types.Message):
    # .strip() убирает лишние пробелы и переносы строк, которые могут ломать URL
    article = message.text.strip().upper()
    await message.answer("Ищем информацию...")

    api_answer = await get_info_async(article)
    # На всякий случай принудительно превращаем в строку
    await message.answer(str(api_answer))


async def main():
    # skip_updates=True позволяет пропустить старые сообщения, которые пришли, пока бот был выключен
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    start()
    asyncio.run(main())