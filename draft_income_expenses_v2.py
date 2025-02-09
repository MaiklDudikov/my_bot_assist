import asyncio
import re
import json
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

# ТВОЙ_ТОКЕН_БОТА
TOKEN = "ТВОЙ_ТОКЕН_БОТА"
DATA_FILE = "finance_data.json"

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загрузка данных из JSON
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"income": {}, "expenses": {}}


# Функция сохранения данных в JSON
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Регулярное выражение для парсинга сообщений
pattern = re.compile(r"(\D+?)\s*(-?\d+)")


# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}. Я бот считающий доходы и расходы.")
    await message.answer("Используй формат : название сумма\n(например : зарплата 5000 или еда -1000)\n"
                         "Проверить баланс /balance")


# Функция для вычисления баланса и категории
def get_balance_info():
    total_income = sum(sum(cat.values()) for cat in data["income"].values())
    total_expenses = sum(sum(cat.values()) for cat in data["expenses"].values())
    balance = total_income - total_expenses

    income_text = "\n".join(
        [f"{cat} : {sum(items.values())} ₽" for cat, items in data["income"].items()]) or "Нет доходов"
    expenses_text = "\n".join(
        [f"{cat} : {sum(items.values())} ₽" for cat, items in data["expenses"].items()]) or "Нет расходов"

    return balance, income_text, expenses_text


# Команда /balance - выводит баланс
@dp.message(Command('balance'))
async def show_balance(message: Message):
    balance, income_text, expenses_text = get_balance_info()

    text = (f"💰 **Баланс** : {balance} ₽\n\n"
            f"📈 **Доходы :**\n{income_text}\n\n"
            f"📉 **Расходы :**\n{expenses_text}")

    await message.reply(text, parse_mode="Markdown")


# Обработчик сообщений (добавление доходов/расходов)
@dp.message()
async def add_transaction(message: Message):
    match = pattern.match(message.text)

    if not match:
        await message.reply("Используй формат : название сумма\nНапример : зарплата 5000 или еда -1000")
        return

    category, amount = match.groups()
    amount = int(amount)

    transaction_type = "income" if amount > 0 else "expenses"
    category = category.strip()
    amount = abs(amount)  # Убираем возможный минус, так как расходы уже хранятся отдельно

    if category not in data[transaction_type]:
        data[transaction_type][category] = {}

    data[transaction_type][category][message.date.timestamp()] = amount
    save_data()

    await message.reply(f"Записано : {category} {amount} ₽")


async def main():
    dp.startup.register(startup)
    await dp.start_polling(bot)


async def startup():
    print('Бот запущен ...')


# Запуск бота
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
