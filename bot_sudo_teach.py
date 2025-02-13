import os
import re
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, CommandObject
from dotenv import load_dotenv
# from config import TOKEN
import openai

# token=TOKEN
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


# @dp.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.answer('Добро пожаловать !')


# С помощью этой команды можно ловить дополнительные параметры, и делать например реферальную систему: t.me/bot?start=123
# t.me/BobReviewBot?start=Maikl_Dudikov
@dp.message(CommandStart(deep_link=True))
async def cmd_start(message: Message, command: CommandObject):
    await message.answer(f'Добро пожаловать, {message.from_user.first_name} ! Ты пришел от {command.args}.')
    await message.answer('Нажми /help')


@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Все команды :\n/start - Приветствие\n/get - передавать с 1 аргументом\n/get2 - передавать с 2 аргументами\n'
                         '/chat - запрос к chatGPT\n\n'
                         'Напиши в чат :\nid - выдаст твоё id\nПривет - выдаст сообщение\nприбыль - посчитает процент прибыли')


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
    await message.answer(f'{message.from_user.first_name}, Ваш ID: {message.from_user.id}')


@dp.message(Command('chat'))
async def cmd_help(message: Message):
    await message.answer(f'{message.from_user.first_name}, что ты хочешь узнать?\n'
                         f'Напиши запрос после слова чат.\n(например : чат как сварить картошку?)')


@dp.message(F.text.startswith('чат '))
async def request_chatgpt(message: Message):
    user_input = message.text[4:].strip()  # Убираем "чат " из текста запроса

    if not user_input:
        await message.answer("Введите запрос после 'чат ', например: 'чат как сварить картошку?'")
        return

    try:
        response = await asyncio.to_thread(openai.ChatCompletion.create,
            model="gpt-3.5-turbo", # Новая актуальная модель (можно заменить на gpt-4-turbo)
            messages=[{"role": "user", "content": user_input}]
        )

        answer = response["choices"][0]["message"]["content"].strip()
        await message.answer(answer if answer else "Не удалось получить ответ 😕")

    except Exception as e:
        await message.answer(f"Ошибка при запросе к ChatGPT: {str(e)}")


# Расчет прибыли в прочентах
@dp.message(F.text.startswith("прибыль"))
async def calculate_profit(message: Message):
    try:
        # Извлекаем числа из сообщения
        numbers = re.findall(r"\d+\.?\d*", message.text)
        if len(numbers) < 2:
            await message.answer(
                "❌ Ошибка! Введите цену покупки и продажи в формате :\nприбыль <цена_покупки> <цена_продажи>\n\nПример : прибыль 1000 1200")
            return

        buy_price, sell_price = map(float, numbers[:2])

        # Расчет процента прибыли
        profit_percent = ((sell_price - buy_price) / buy_price) * 100

        # Форматируем ответ
        result_text = f"💰 **Прибыль** : {profit_percent:.2f}%"
        await message.answer(result_text, parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"⚠ Ошибка при расчете : {e}")


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
