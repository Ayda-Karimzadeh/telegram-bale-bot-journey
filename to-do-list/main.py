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

def add(message):
    
    sent = bot.send_message(message.chat.id, "Add a task.")
    bot.register_next_step_handler(sent,add_task)

def add_task(message):
    task = message.text
    user_id = message.from_user.id
    database.add_task(user_id=user_id, task=task)
    bot.send_message(message.chat.id, "✅ noted.")
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    database.insert_user(user_id=user_id, user_name=user_name)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_btn = types.KeyboardButton('Add Task')
    list_btn = types.KeyboardButton('List')
    stats_btn = types.KeyboardButton('Stats')
    keyboard.add(add_btn,list_btn,stats_btn)

    bot.send_message(message.chat.id,
        f"Welcome to To do list bot *{user_name}* .", reply_markup=keyboard)

@bot.message_handler(func= lambda message: message.text in ["Add Task", "List", "Stats"])
def buttons_handler(message):
    if message.text == 'Add Task':
        add(message)
        
    elif message.text == 'List':
        tasks =database.get_list(user_id=message.from_user.id)

        if not tasks:
            bot.send_message(message.chat.id, "No task found.")
        else:
            buttons = []
            markup = types.InlineKeyboardMarkup()

            for name, datetime in tasks:
                btn = types.InlineKeyboardButton(f"{name} ○",callback_data=name)
                buttons.append(btn)

            for btn in buttons:
                markup.add(btn)

            bot.send_message(message.chat.id,"📋 Your list:",reply_markup=markup)

        
    else:
        stats = database.get_stats(user_id=message.from_user.id)

        if not stats:
            bot.send_message(message.chat.id, "No task found.")

        else:
            bot.send_message(message.chat.id,f"You have {stats} tasks waiting to be done.")
        

    
@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, "🤔")

bot.infinity_polling()