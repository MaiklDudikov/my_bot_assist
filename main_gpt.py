import os
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# Загружаем API-ключи из .env файла
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

# Создание бота и диспетчера (aiogram 3.7.0)
bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет, {hbold(message.from_user.first_name)}! Я бот ChatGPT. Напиши мне что-нибудь!")


# Обработчик текстовых сообщений
@dp.message()
async def chat_with_gpt(message: Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
            max_tokens=100
        )
        reply_text = response["choices"][0]["message"]["content"]
        await message.answer(reply_text)
    except Exception as e:
        await message.answer("Ошибка при обработке запроса: " + str(e))


# Функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
