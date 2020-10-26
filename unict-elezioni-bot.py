from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

import json

def logging_message(update: Update, context: CallbackContext):
    try:
        message_id = update.message.message_id #ID MESSAGGIO
        user = update.message.from_user # Restituisce un oggetto Telegram.User
        chat = update.message.chat # Restituisce un oggetto Telegram.Chat
        text = update.message.text #Restituisce il testo del messaggio
        date = update.message.date #Restituisce la data dell'invio del messaggio
        message = "\n___ID MESSAGE: "+ str(message_id) + "____\n" + \
                    "___INFO USER___\n" + \
                    "user_id:"+ str(user.id) + "\n" + \
                    "user_name:"+ str(user.username) + "\n" + \
                    "user_firstlastname:" + str(user.first_name) + " " + str(user.last_name) + "\n" + \
                    "___INFO CHAT___\n" + \
                    "chat_id:"+ str(chat.id) + "\n" + \
                    "chat_type:"+ str(chat.type)+"\n" + "chat_title:" + str(chat.title) + "\n" + \
                    "___TESTO___\n" + \
                    "text:"+ str(text) + "\n" + \
                    "date:"+ str(date) + \
                    "\n_____________\n"
        log_tmp = open("logs/logs.txt","a+")
        log_tmp.write("\n"+message)
    except ValueError:
        pass

def get_link(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'https://unict-dmi.github.io/UNICT-Elezioni')

def start(update, context) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Link", callback_data='/link')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "/link":
        get_link(query, context)

def get_token() -> str:
    content = None
    with open("./config/config.json", 'r') as config_file:
        content = config_file.read()
    configs = json.loads(content)
    return configs['TOKEN']

def main() -> None:
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.all, logging_message),1)
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('menu', start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(CommandHandler('link', get_link))
    updater.start_polling()
    updater.idle()

TOKEN = get_token()

if __name__ == "__main__":
    main()