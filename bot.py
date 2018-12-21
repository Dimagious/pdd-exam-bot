# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, RegexHandler
from random import randint
import logging
import messages
import config
import db

logging.basicConfig(format=messages.LOGGING, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(config.TOKEN, request_kwargs=config.PROXY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start, pass_user_data=True))
    dp.add_handler(CommandHandler("training", training, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Вернуться в меню)$', start, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Следующий вопрос️)$', training, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(user_answer))
    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TOKEN)
    # updater.bot.set_webhook("https://pdd-exam-bot.herokuapp.com/" + TOKEN)
    updater.idle()


def start(bot, update, user_data):
    """
    Метод, который представляет собой главное меню бота
    :param bot:
    :param update:
    :param user_data:
    """
    bot.sendMessage(chat_id=update.message.chat_id, text=messages.WELCOME)


def help(bot, update, user_data):
    """
    Метод, который посылает пользователю информацию о своих режимах работы и функциях
    :param bot:
    :param update:
    :param user_data:
    """
    bot.sendMessage(chat_id=update.message.chat_id, text=messages.HELP)


def user_answer(bot, update):
    """
    Метод, который в зависимости от ответа пользователя использует опредеённую логику
    :param bot:
    :param update:
    """
    keyboard = [
        [InlineKeyboardButton(messages.NEXT, callback_data='7')],
        [InlineKeyboardButton(messages.MENU, callback_data='5')]
    ]

    query = update.callback_query
    user_choice = int(query.data.split(';')[0])
    ticket = int(query.data.split(';')[1])
    question = int(query.data.split(';')[2])
    comment = db.get_comment(ticket, question)
    write_choice = int(db.get_write_answer(ticket, question))

    if user_choice == 5:
        bot.sendMessage(chat_id=query.message.chat.id, text=messages.WELCOME,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))
    elif user_choice == 6:
        bot.sendMessage(chat_id=query.message.chat.id, text=comment,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))
    elif user_choice == 7:
        bot.sendMessage(chat_id=query.message.chat_id, text=db.get_question(ticket, question),
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))
    elif user_choice == write_choice:
        bot.sendMessage(text='Верно! \n\n' + comment, chat_id=query.message.chat.id,
                        message_id=query.message.message_id,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))
    else:
        bot.sendMessage(text='Неверно! \n\n' + comment, chat_id=query.message.chat.id,
                        message_id=query.message.message_id,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))


def training(bot, update, user_data):
    """
    Метод, который посылает случайный вопрос из случайного билета пользователю
    :param bot:
    :param update:
    :param user_data:
    """
    random_ticket = 1
    random_question = randint(1, 20)

    three_answers = [[
        InlineKeyboardButton(messages.ONE, callback_data='1;' + str(random_ticket) + ';' + str(random_question)),
        InlineKeyboardButton(messages.TWO, callback_data='2;' + str(random_ticket) + ';' + str(random_question)),
        InlineKeyboardButton(messages.THREE, callback_data='3;' + str(random_ticket) + ';' + str(random_question))
    ]]

    four_answers = [[
        InlineKeyboardButton(messages.ONE, callback_data='1;' + str(random_ticket) + ';' + str(random_question)),
        InlineKeyboardButton(messages.TWO, callback_data='2;' + str(random_ticket) + ';' + str(random_question)),
        InlineKeyboardButton(messages.THREE, callback_data='3;' + str(random_ticket) + ';' + str(random_question)),
        InlineKeyboardButton(messages.FOUR, callback_data='4;' + str(random_ticket) + ';' + str(random_question))
    ]]

    choices = db.get_number_of_choices(random_ticket, random_question)

    reply_markup = InlineKeyboardMarkup(three_answers) if int(choices) == 3 else InlineKeyboardMarkup(four_answers)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=db.get_question(random_ticket, random_question),
                    reply_markup=reply_markup)


if __name__ == '__main__':
    main()
