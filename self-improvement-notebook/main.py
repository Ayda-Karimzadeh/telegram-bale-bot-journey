import telebot
import os
import logging
import database
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}'

API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

database.init_db()

def add():
    pass
    

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_btn = types.KeyboardButton('Add')
    list_btn = types.KeyboardButton('List')
    stats_btn = types.KeyboardButton('Stats')
    keyboard.add(add_btn,list_btn,stats_btn)

    bot.send_message(message.chat.id,
        "Welcome to Grow Track bot.", reply_markup=keyboard)

@bot.message_handler(func= lambda message:True)
def handler(message):
    if message.text == 'Add' or 'add' or 'ADD':
        add()
    else:
        bot.send_message(message.chat.id, ":/")

bot.infinity_polling()