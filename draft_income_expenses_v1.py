import json
import os
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
import asyncio

# YOUR_TELEGRAM_BOT_TOKEN
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
DATA_FILE = "finance_data.json"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Загружаем данные
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"income": [], "expenses": []}


# Функция сохранения данных в JSON
def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Обработка сообщений с доходами и расходами
@dp.message()
async def handle_transaction(message: types.Message):
    text = message.text.lower()
    
    if text.startswith("доход"):
        parts = text.split()
        if len(parts) >= 3:
            amount = int(parts[1])
            category = " ".join(parts[2:])
            data["income"].append({"amount" : amount, "category" : category})
            save_data()
            await message.reply(f"✅ Доход {amount} ₽ добавлен в категорию '{category}'")
    
    elif text.startswith("расход"):
        parts = text.split()
        if len(parts) >= 3:
            amount = int(parts[1])
            category = " ".join(parts[2:])
            data["expenses"].append({"amount" : amount, "category" : category})
            save_data()
            await message.reply(f"❌ Расход {amount} ₽ добавлен в категорию '{category}'")
    
    elif text == "баланс":
        total_income = sum(item["amount"] for item in data["income"])
        total_expense = sum(item["amount"] for item in data["expenses"])
        balance = total_income - total_expense
        await message.reply(f"📊 Баланс : {balance} ₽\nДоходы : {total_income} ₽\nРасходы : {total_expense} ₽")
    
    elif text == "график":
        if not data["expenses"] and not data["income"]:
            await message.reply("Нет данных для построения графика.")
            return
        
        categories_income = {}
        for item in data["income"]:
            categories_income[item["category"]] = categories_income.get(item["category"], 0) + item["amount"]
        
        categories_expense = {}
        for item in data["expenses"]:
            categories_expense[item["category"]] = categories_expense.get(item["category"], 0) + item["amount"]
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        
        if categories_income:
            ax[0].pie(categories_income.values(), labels=categories_income.keys(), autopct='%1.1f%%', startangle=140)
            ax[0].set_title("Доходы по категориям")
        
        if categories_expense:
            ax[1].pie(categories_expense.values(), labels=categories_expense.keys(), autopct='%1.1f%%', startangle=140)
            ax[1].set_title("Расходы по категориям")
        
        plt.savefig("finance_chart.png")
        plt.close()
        
        # with open("finance_chart.png", "rb") as photo:
        #     await message.reply_photo(photo, caption="📊 График доходов и расходов")

        photo = FSInputFile("finance_chart.png")
        await message.answer_photo(photo, caption="📊 График доходов и расходов")
    
    else:
        await message.reply("❓ Используйте команды :\n- 'доход 5000 зарплата'\n- 'расход 1000 еда'\n- 'баланс'\n- 'график'")


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
