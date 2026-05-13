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
    
    sent = bot.send_message(message.chat.id, "Add a progress.")
    bot.register_next_step_handler(sent,add_pro)

def add_pro(message):
    progress = message.text
    user_id = message.from_user.id
    database.add_progress(user_id=user_id, progress=progress)
    bot.send_message(message.chat.id, "✅ Saved.")
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    database.insert_user(user_id=user_id, user_name=user_name)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_btn = types.KeyboardButton('Add')
    list_btn = types.KeyboardButton('List')
    stats_btn = types.KeyboardButton('Stats')
    keyboard.add(add_btn,list_btn,stats_btn)

    bot.send_message(message.chat.id,
        f"Welcome to Grow Track bot *{user_name}* .", reply_markup=keyboard)

@bot.message_handler(func= lambda message: message.text in ["Add", "List", "Stats"])
def buttons_handler(message):
    if message.text == 'Add':
        add(message)
        
    elif message.text == 'List':
        progresses =database.get_list(user_id=message.from_user.id)

        if not progresses:
            bot.send_message(message.chat.id, "No progress found.")
        else:
            lines = []
            for name, datetime in progresses:
                date, time = datetime.split()
                lines.append(f"• {name} — {date} at {time}")

            final_message = "📋 Your list :\n\n" + "\n".join(lines)
            bot.send_message(message.chat.id,final_message)
        
    else:
        stats = database.get_stats(user_id=message.from_user.id)

        if not stats:
            bot.send_message(message.chat.id, "No progress found.")

        else:
            bot.send_message(message.chat.id,f"You have {stats} progresses. ✌️")
        

    
@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, "😐")

bot.infinity_polling()