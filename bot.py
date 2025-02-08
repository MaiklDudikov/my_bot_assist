import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv
# from config import TOKEN

# token=TOKEN
load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать !')


@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Чем я могу помочь ?')


@dp.message(F.text == 'Привет')
async def hello(message: Message):
    await message.reply('Как дела ?')


# @dp.message()
# async def echo(message: Message):
#     await message.answer('В разработке ...')


async def main():
    dp.startup.register(startup)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    print('Бот запущен ...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
