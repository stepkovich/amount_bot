import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from get_data import get_info, get_sertificats, get_analog

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

artt = {"chat": "",
        "massage": ""}


def start():
    print('Bot starting')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Введите артикул:")


@dp.message_handler()
async def get_article_data(message: types.Message):
    # global artt
    m = message.text.upper()
    id_chat = message.chat.id
    inf = {"chat": id_chat,
           "massage": m}
    artt.update(inf)
    # print(artt.get("massage"))
    ikb = InlineKeyboardMarkup(row_width=2)
    b1 = InlineKeyboardButton(text="Цена и наличие", callback_data="info")
    b2 = InlineKeyboardButton(text="Сертификаты", callback_data="sert")
    b3 = InlineKeyboardButton(text="Аналоги", callback_data="analog")
    ikb.add(b1, b2, b3)
    await message.reply("Какая информация необходима?", reply_markup=ikb)


@dp.callback_query_handler(text="info")
async def sew(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer(get_info(artt.get("massage")), )


@dp.callback_query_handler(text="sert")
async def sew(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer(get_sertificats(artt.get("massage")))


@dp.callback_query_handler(text="analog")
async def sew(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer(f'Аналоги для: -----> {artt}\n{get_analog(artt)}')


if __name__ == '__main__':
    start()
    executor.start_polling(dp, skip_updates=True)
