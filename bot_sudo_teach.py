import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from dotenv import load_dotenv
# from config import TOKEN

# token=TOKEN
load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать !')


# С помощью этой команды можно ловить дополнительные параметры, и делать например реферальную систему: t.me/bot?start=123
# t.me/BobReviewBot?start=Maikl_Dudikov
# @dp.message(CommandStart(deep_link=True))
# async def cmd_start(message: Message, command: CommandObject):
#     await message.answer(f'Привет {message.from_user.first_name} ! Ты пришел от {command.args}')
#     await message.answer('Добро пожаловать ! Нажми /help')


@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Все команды :\n/start - Приветствие\n/get - передавать с 1 аргументом\n/get2 - передавать с 2 аргументами\n\n'
                         'Напиши в чат :\nid - выдаст твоё id\nПривет - выдаст сообщение')


# noinspection PyBroadException
@dp.message(Command('get2'))
async def cmd_get2(message: Message, command: CommandObject):
    if not command.args:
        await message.answer('Аргументы не переданы')
        return
    try:
        value1, value2 = command.args.split(' ', maxsplit=1)
        await message.answer(f'Вы ввели команду help с аргументом {value1} {value2}')
    except:
        await message.answer('Были введены неправильные аргументы')


@dp.message(Command('get'))
async def cmd_get(message: Message, command: CommandObject):
    await message.answer(f'Вы ввели команду get с аргументом {command.args}')


@dp.message(F.text == 'Привет')
async def hello(message: Message):
    await message.reply('Привет, как дела ?')
    await message.answer('Чем я могу помочь ?')


@dp.message(F.text.startswith('id'))
async def get_id(message: Message):
    await message.answer(f'{message.from_user.first_name}, вам нужна помощь?')
    await message.answer(f'Ваш ID: {message.from_user.id}')


# @dp.message()
# async def echo(message: Message):
#     await message.answer('В разработке ...')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(startup)
    await dp.start_polling(bot)


async def startup():
    print('Бот запущен ...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
