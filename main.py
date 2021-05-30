from datetime import datetime

import telebot
from pycbrf import ExchangeRates

import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    item3 = types.KeyboardButton("USD")
    item4 = types.KeyboardButton("EUR")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, который с радостью ответит на вопрос \"Как дела?\", выведет рандомное число и покажет курс валют!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def msg(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊 Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        elif message.text == 'EUR':
            coinEur = 'EUR'
            rates = ExchangeRates(datetime.now())
            bot.send_message(message.chat.id, str(rates[coinEur].rate))

        elif message.text == 'USD':
            coinUsd = 'USD'
            rates = ExchangeRates(datetime.now())
            bot.send_message(message.chat.id, str(rates[coinUsd].rate))
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢 Нажми на кнопку, которая тебя интересует!')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько! 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Не переживай, всё наладится! 😢')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
