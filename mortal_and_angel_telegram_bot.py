import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import telebot
import requests


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# initialize the bot using ID
bot = telebot.TeleBot('placeholder for telegram bot ID')

CHOOSING, CHAT_WITH_ANGEL, TYPING_REPLY_TO_ANGEL, TYPING_REPLY_TO_MORTAL, TYPING_REPLY_TO_ADMIN, LOCATION, BIO = range(7)
reply_keyboard = [['Talk to whale', 'Talk to fish', 'Talk to admin']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


### Change here -- START

admin_id = 'placeholder for tele ID' # admin id


# 'first_name': 'id', 
user_id_pair = {
    'first_name1': 'placeholder for id',
    'first_name2': 'placeholder for id',
    'sample': 'tele_id',
}

# 'first_name': ['first_name's whale, 'first_name's fish'],
angel_mortal_dict = {
    'first_name1' : ['first_name2', 'first_name2'],
    'first_name2': ["first_name1", 'first_name1'],
    'sample': ["sample's whale", "sample's fish"],
}

### Change here -- END


def start(update, context):
    user_firstname = update.message.from_user.first_name
    user_id = update.message.from_user.id

    update.message.reply_text(
        f'Hi {user_firstname}! I am your messenger. \n'
            'Choose whom you want to send your message to.', reply_markup=markup)

    return CHOOSING

# Sends a text message to a user's whale.
def chat_with_angel(update, context):
    user = update.message.from_user
    text = update.message.text

    logger.info("%s says to his/her whale: %s", user.first_name, update.message.text)

    update.message.reply_text('Craft your message to your whale and I will deliver your message.',
                              reply_markup=ReplyKeyboardRemove())

    return TYPING_REPLY_TO_ANGEL

# Sends a text message to a user's fish.
def chat_with_mortal(update, context):
    user = update.message.from_user
    # update.message.text
    text = update.message.text

    logger.info("%s says to his/her fish: %s", user.first_name, update.message.text)

    update.message.reply_text('Craft your message to your fish and I will deliver your message.',
                              reply_markup=ReplyKeyboardRemove())

    return TYPING_REPLY_TO_MORTAL

# Sends a text message to admin.
def chat_with_admin(update, context):
    user = update.message.from_user
    # update.message.text
    text = update.message.text

    logger.info("%s says to his/her admin: %s", user.first_name, update.message.text)

    update.message.reply_text('Craft your message to admin and I will deliver your message.',
                              reply_markup=ReplyKeyboardRemove())

    return TYPING_REPLY_TO_ADMIN

def send_to_angel(update, context):
    user = update.message.from_user
    update.message.text
    text = update.message.text
    msg = "You received the following message from your fish!"

    angel_name = angel_mortal_dict[user.first_name][0]
    angel_id = user_id_pair[angel_name]

    logger.info("%s sent this message: %s", user.first_name, update.message.text)
    requests.get(f"https://api.telegram.org/bot854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls/sendMessage?chat_id={angel_id}&text={msg}")
    requests.get(f"https://api.telegram.org/bot854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls/sendMessage?chat_id={angel_id}&text={text}")
    update.message.reply_text("Sweet! We have delivered the message:\n{}".format(text), reply_markup=markup)

    return CHOOSING

def send_to_mortal(update, context):
    user = update.message.from_user
    update.message.text
    text = update.message.text
    msg = "You received the following message from your whale!"

    mortal_name = angel_mortal_dict[user.first_name][1]
    mortal_id = user_id_pair[mortal_name]

    logger.info("%s sent this message to %s : %s", user.first_name, mortal_name, update.message.text)
    requests.get(f"https://api.telegram.org/bot854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls/sendMessage?chat_id={mortal_id}&text={msg}")
    requests.get(f"https://api.telegram.org/bot854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls/sendMessage?chat_id={mortal_id}&text={text}")
    update.message.reply_text("Sweet! We have delivered the message:\n{}".format(text), reply_markup=markup)

    return CHOOSING

def send_to_admin(update, context):
    user = update.message.from_user
    update.message.text
    text = update.message.text
    msg = f"You received the following message from {user.first_name}."

    logger.info("%s sent this message to admin: %s", user.first_name, update.message.text)

    x = requests.get(f"https://api.telegram.org/bot854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls/sendMessage?chat_id={admin_id}&text={msg}")
    x = requests.get(f"https://api.telegram.org/bot854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls/sendMessage?chat_id={admin_id}&text={text}")

    update.message.reply_text("Sweet! We have delivered the message:\n{}".format(text), reply_markup=markup)

    return CHOOSING


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("854952340:AAF0wn1QZDNlvsXG2tr91VkuQhXTmZV1xls", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^Talk to whale$',
                                    chat_with_angel),
                                    # pass_user_data=True),
                       RegexHandler('^Talk to fish$',
                                    chat_with_mortal),
                       RegexHandler('^Talk to admin$',
                                    chat_with_admin),
                       ],

            TYPING_REPLY_TO_ANGEL: [MessageHandler(Filters.text, send_to_angel)],
            TYPING_REPLY_TO_MORTAL: [MessageHandler(Filters.text, send_to_mortal)],
            TYPING_REPLY_TO_ADMIN: [MessageHandler(Filters.text, send_to_admin)],
        },

        fallbacks=[RegexHandler('^cancel$', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


#pip install python-telegram-bot