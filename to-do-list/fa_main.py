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

# load database
database.init_db()

# main menu keyboard
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    add_btn = types.KeyboardButton('افزودن کار')
    stats_btn = types.KeyboardButton('آمار')
    del_btn = types.KeyboardButton('حذف کردن')
    list_btn = types.KeyboardButton('لیست کارها')
    keyboard.add(add_btn,stats_btn,del_btn,list_btn)
    return keyboard

# to do list inline buttons
def create_task_markup(user_id):
    tasks = database.get_list(user_id)
    markup = types.InlineKeyboardMarkup()
    for name, task_id, status in tasks:
        icon = "●" if status == 1 else "○"
        btn = types.InlineKeyboardButton(f"{name} {icon}", callback_data=str(task_id))
        markup.add(btn)
    return markup

def del_tasks_inkey(user_id):
    tasks = database.get_list(user_id)
    markup = types.InlineKeyboardMarkup()
    for name, task_id, status in tasks:
        icon = "●" if status == 1 else "○"
        btn = types.InlineKeyboardButton(f"{name} {icon} 🗑️", callback_data=str(task_id))
        markup.add(btn)
    return markup

# add menu keyboard
def add_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_added = types.KeyboardButton("ثبت کارها")
    btn_menu = types.KeyboardButton("بازگشت")
    keyboard.add(btn_added,btn_menu)
    return keyboard

# handle start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    database.insert_user(user_id=user_id, user_name=user_name)
    #agar karbar jadid nabood pyam motefaveti neshan dahad
    bot.send_message(message.chat.id,
        f"سلام به ربات لیست کارها خوش آمدی*{user_name}*.\n\n"
        "از دکمه‌های زیر برای افزودن کار، مشاهده لیست و آمار استفاده کن."
        , reply_markup=main_menu(),parse_mode="Markdown")
    
# callback query handler
@bot.callback_query_handler(func= lambda call: call.data.isdigit())       
def callback_handler(call):
    task_id = int(call.data)
    user_id = call.from_user.id
    user_state = database.get_user_state(user_id)

    if user_state == "to do list":

        database.update_task_status(task_id,user_id)
        markup = create_task_markup(user_id)

        try :
            bot.edit_message_text(
                chat_id = call.message.chat.id,message_id = call.message.message_id,
                text = "📋 لیست شما :",reply_markup = markup
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")

    elif user_state == "deleting tasks":
        database.del_task(task_id,user_id)
        markup = del_tasks_inkey(user_id)
        try:
            if not database.get_list(user_id):
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="لیست شما خالی است.")
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="لیست شما:", reply_markup=markup)
        except Exception as e:
            logger.error(f"Error editing message: {e}")

    bot.answer_callback_query(call.id)
    
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    user_state = database.get_user_state(user_id)
    if message.text == "افزودن کار":
        num_tasks = database.count_tasks(user_id)
        if num_tasks < 10 :
            database.update_user_state(user_id,"adding task")
            bot.send_message(message.chat.id,
                                "کارهای خودت را وارد کن.\n"
                                "وقتی تمام شد روی *ثبت کارها* بزن.",
                                reply_markup=add_menu(),
                                parse_mode="Markdown")
            return
        else:
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id,"متأسفم، به محدودیت رسیدی.\n"
                                            "شما فقط می‌توانید ۱۰ کار در لیست خود داشته باشید.", reply_markup=main_menu())

    elif user_state == "adding task":
        if message.text == "ثبت کارها":
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id, "تمامی کارها ثبت شدند.", reply_markup=main_menu())

        elif message.text == "بازگشت":
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id, "بازگشت به منوی اصلی.", reply_markup=main_menu())

        else:
            num_tasks = database.count_tasks(user_id)
            if num_tasks < 10:
                database.add_task(user_id=user_id, task=message.text)
            else:
                database.update_user_state(user_id, "none")
                bot.send_message(message.chat.id,"متأسفم، محدودیت ۱۰ کار رعایت شود. کارهای قبلی ذخیره شدند، اما آخرین کار ذخیره نشد.",
                                reply_markup=main_menu())
            return

    elif message.text == "لیست کارها":
        database.update_user_state(user_id,"to do list")
        tasks = database.get_list(user_id=user_id)
        if not tasks:
            bot.send_message(message.chat.id, "لیست شما خالی است.")
        else:
            markup = create_task_markup(user_id)
            bot.send_message(message.chat.id, "📋 لیست شما:", reply_markup=markup)
        return

    # task hay anjam shode va nashode neshan dahad adad ya masalan nemoodar
    elif message.text == "آمار":
        tasks = database.get_list(user_id)
        if not tasks:
            bot.send_message(message.chat.id, "لیست شما خالی است.")
        else:
            stats = database.get_stats(user_id=user_id)
            bot.send_message(message.chat.id, f"شما {stats} کار انجام‌نشده دارید.")
        return
    
    elif message.text == "حذف کردن":
        database.update_user_state(user_id, "deleting tasks")
        
        # ۱. ساخت کیبورد متنی برای گزینه‌های کلی
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        del_mylist_btn = types.KeyboardButton('حذف کل لیست')
        back_btn = types.KeyboardButton('بازگشت')
        keyboard.add(del_mylist_btn, back_btn)
        
        # ۲. گرفتن لیست تسک‌ها و ساخت مارک‌آپ این‌لاین
        tasks = database.get_list(user_id)
        if not tasks:
            bot.send_message(message.chat.id, "لیست شما خالی است.", reply_markup=keyboard)
        else:
            # ۳. ارسال تنها یک پیام که هم شامل توضیح است و هم دکمه‌های این‌لاین
            bot.send_message(message.chat.id, "برای حذف کار روی آن کلیک کن.", reply_markup=keyboard)
            bot.send_message(message.chat.id, "لیست شما:", reply_markup=del_tasks_inkey(user_id))


    elif user_state == "deleting tasks":
        
        if message.text == "حذف کل لیست":
            database.del_all_tasks(user_id)
            database.update_user_state(user_id, "none")
            bot.send_message(message.chat.id,"لیست کارهای شما با موفقیت حذف شد!", reply_markup=main_menu())

        elif message.text == "بازگشت":
            database.update_user_state(user_id,"none")
            bot.send_message(message.chat.id, "بازگشت به منوی اصلی.", reply_markup=main_menu())
            return

    elif message.text == "بازگشت":
        database.update_user_state(user_id,"none")
        bot.send_message(message.chat.id, "بازگشت به منوی اصلی.", reply_markup=main_menu())
        return
    
    else:
        bot.send_message(message.chat.id, "🤔")

bot.infinity_polling()