import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

TOKEN = "ТВОЙ_ТОКЕН_БОТА"

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Хранение данных (доходы, расходы)
data = {"income": [], "expenses": []}

# Регулярное выражение для парсинга сообщений
pattern = re.compile(r"(\D+?)\s*(-?\d+)")


# Обработчик сообщений (добавление доходов/расходов)
@dp.message_handler()
async def add_transaction(message: Message):
    match = pattern.match(message.text)
    
    if not match:
        await message.reply("Используй формат: <название> <сумма>\nПример: зарплата 5000 или еда -1000")
        return

    category, amount = match.groups()
    amount = int(amount)

    if amount > 0:
        data["income"].append((category, amount))
    else:
        data["expenses"].append((category, amount))

    await message.reply(f"Записано: {category} {amount} ₽")


# Команда /balance - выводит баланс
@dp.message_handler(commands=["balance"])
async def show_balance(message: Message):
    total_income = sum(i[1] for i in data["income"])
    total_expenses = sum(e[1] for e in data["expenses"])
    balance = total_income + total_expenses  # Расходы хранятся с минусом

    income_text = "\n".join([f"{i[0]}: {i[1]} ₽" for i in data["income"]]) or "Нет доходов"
    expenses_text = "\n".join([f"{e[0]}: {e[1]} ₽" for e in data["expenses"]]) or "Нет расходов"

    text = (f"💰 **Баланс**: {balance} ₽\n\n"
            f"📈 **Доходы:**\n{income_text}\n\n"
            f"📉 **Расходы:**\n{expenses_text}")

    await message.reply(text, parse_mode="Markdown")

# Запуск бота
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
