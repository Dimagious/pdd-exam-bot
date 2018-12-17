# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from random import randint
import logging
import messages
import config
import db

CHOOSE_MODE = range(1)
logging.basicConfig(format=messages.LOGGING, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(config.TOKEN, request_kwargs=config.PROXY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("start_training", start_training))
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TOKEN)
    # updater.bot.set_webhook("https://pdd-exam-bot.herokuapp.com/" + TOKEN)
    updater.idle()


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=messages.WELCOME)


def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, messages.STOP)
    return ConversationHandler.END


def start_training(bot, update):
    three_answers = [[InlineKeyboardButton("1", callback_data='1'), InlineKeyboardButton("2", callback_data='2'),
                      InlineKeyboardButton("3", callback_data='3')]]
    four_answers = [[InlineKeyboardButton("1", callback_data='1'), InlineKeyboardButton("2", callback_data='2'),
                     InlineKeyboardButton("3", callback_data='3'), InlineKeyboardButton("4", callback_data='4')]]
    random_number = randint(0, 20)
    choices = db.get_number_of_choices(0, random_number)

    reply_markup = InlineKeyboardMarkup(three_answers) if choices == 3 else InlineKeyboardMarkup(four_answers)

    bot.sendMessage(chat_id=update.message.chat_id, text=db.get_question(0, random_number),
                    reply_markup=reply_markup, one_time_keyboard=True)


if __name__ == '__main__':
    main()
