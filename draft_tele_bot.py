import telebot
import openai
import time
from datetime import datetime
from gtts import gTTS
import os

telegram_token = '19:AA'
openai.api_key = 'sk-xv'
admin_id = 1678086777
# Майкл Дудиков! Иван Косенко! Женя Шемчук! Андрей Бел.! Слава Пьяных!
users = [1678086777, 255228821, 5241864093, 1988065384, 1897715059]
# Илья Ареф 767815540 ???? Алик Бровкин 2118550742 !!!!!
# Челохсаев 1254349681 ??? Максим Братухин 1362043435???
bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот на основе искуственного интеллекта chatGPT, готовый помочь Вам. Просто напишите мне что-нибудь!")


@bot.message_handler(commands=['send_voice'])
def send_voice(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, "Рассылка началась!")
        for i in users:
            text = message.text[message.text.find(' '):]
            tts = gTTS(text, lang='ru')
            tts.save('prognos.mp3')

            with open("prognos.mp3", 'rb') as audio:
                bot.send_voice(i, audio)

            os.remove("prognos.mp3")

        bot.send_message(message.chat.id, "Закончилась!")
    else:
        bot.send_message(message.chat.id, "Ошибка!")


@bot.message_handler(commands=['send_voice_one'])
def send_voice_one(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, "Рассылка началась!")

        text = message.text[message.text.find('-'):]
        tts = gTTS(text, lang='ru', tld='es')
        tts.save('prognos.mp3')
        user_id = message.text[message.text.find(''):].split()[1]

        with open("prognos.mp3", 'rb') as audio:
            bot.send_voice(user_id, audio)

        os.remove("prognos.mp3")

        bot.send_message(message.chat.id, "Закончилась!")
    else:
        bot.send_message(message.chat.id, "Ошибка!")


@bot.message_handler(commands=['send_text'])
def send_text(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, "Рассылка началась!")

        for i in users:
            bot.send_message(i, message.text[message.text.find(' '):])

        bot.send_message(message.chat.id, "Закончилась!")
    else:
        bot.send_message(message.chat.id, "Ошибка!")


@bot.message_handler(commands=['send_text_one'])
def send_text_one(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, "Рассылка началась!")
        user_id = message.text[message.text.find(''):].split()[1]

        bot.send_message(user_id, message.text[message.text.find('-'):])

        bot.send_message(message.chat.id, "Закончилась!")
    else:
        bot.send_message(message.chat.id, "Ошибка!")


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    user_input = message.text
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    current_datetime = datetime.now()
    print(current_datetime, user_name, user_id, user_input)

    bot.send_message(1678086777, f"{user_name} {user_id}\n{user_input}")

# response = openai.Completion.create(
# engine="text-davinci-003",
# prompt=user_input,
# max_tokens=1000  # Максимальная длина ответа от ChatGPT
# )

# bot.send_message(message.chat.id, response.choices[0].text)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(10)
