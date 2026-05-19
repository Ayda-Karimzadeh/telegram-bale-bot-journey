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

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_btn = types.KeyboardButton('Add Task')
    list_btn = types.KeyboardButton('List Tasks')
    stats_btn = types.KeyboardButton('Stats')
    keyboard.add(add_btn,list_btn,stats_btn)
    return keyboard

def create_task_markup(tasks):
    markup = types.InlineKeyboardMarkup()
    for name, task_id, status in tasks:
        icon = "●" if status == 1 else "○"
        btn = types.InlineKeyboardButton(f"{name} {icon}", callback_data=str(task_id))
        markup.add(btn)
    return markup

def add_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_added = types.KeyboardButton("Tasks added")
    btn_menu = types.KeyboardButton("Back")
    keyboard.add(btn_added,btn_menu)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    database.insert_user(user_id=user_id, user_name=user_name)
    #agar karbar jadid nabood pyam motefaveti neshan dahad
    bot.send_message(message.chat.id,
        f"Welcome to To do list bot *{user_name}*.\n\n"
        "Use the buttons below to add tasks, see your list, and view stats."
        , reply_markup=main_menu(),parse_mode="Markdown")

@bot.callback_query_handler(func= lambda call: call.data.isdigit())       
def callback_handler(call):
    task_id = int(call.data)
    user_id = call.from_user.id
    database.update_task_status(task_id,user_id)

    tasks = database.get_list(user_id=user_id)
    markup = create_task_markup(tasks)

    try :
        bot.edit_message_text(
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            text = "📋 Your list :",
            reply_markup = markup
        )
    except Exception as e:
        logger.error(f"Error editing message: {e}")

    bot.answer_callback_query(call.id)
    
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    user_state = database.get_user_state(user_id)
    if message.text == "Add Task":
        database.update_user_state(user_id,"adding task")
        bot.send_message(message.chat.id,
                            "Add tasks. when you are done click *Tasks added*.",
                            reply_markup=add_menu(),
                            parse_mode="Markdown")
        return
    elif user_state == "adding task":
        if message.text == "Tasks added":
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id, "All tasks saved.", reply_markup=main_menu())

        elif message.text == "Back":
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id, "Back to main menu.", reply_markup=main_menu())

        else:
            database.add_task(user_id=user_id, task=message.text)
            return

    elif message.text == "List Tasks":
        tasks = database.get_list(user_id=user_id)
        if not tasks:
            bot.send_message(message.chat.id, "No task found.")
        else:
            markup = create_task_markup(tasks)
            bot.send_message(message.chat.id, "📋 Your list:", reply_markup=markup)
        return

    # task hay anjam shode va nashode neshan dahad adad ya masalan nemoodar
    elif message.text == "Stats":
        stats = database.get_stats(user_id=user_id)
        if not stats:
            bot.send_message(message.chat.id, "No task found.")
        else:
            bot.send_message(message.chat.id, f"You have {stats} tasks waiting to be done.")
        return
    
    elif message.text == "Back":
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id, "Back to main menu.", reply_markup=main_menu())
            return
    else:
        bot.send_message(message.chat.id, "🤔")

# ezafe kardan delete

bot.infinity_polling()