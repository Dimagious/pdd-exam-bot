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
    dp.add_handler(CommandHandler("exam", exam, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Вернуться в меню)$', start, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Следующий вопрос️)$', training, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Пересдать экзамен️)$', exam, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(user_answer))
    updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=config.PORT,
                          url_path=config.TOKEN)
    updater.bot.set_webhook("https://pdd-exam-bot.herokuapp.com/" + config.TOKEN)
    updater.idle()


def start(bot, update, user_data):
    """
    Метод, который представляет собой главное меню бота
    :param bot:
    :param update:
    :param user_data:
    """
    bot.sendMessage(chat_id=update.message.chat_id, text=messages.WELCOME)


def training(bot, update, user_data):
    """
    Метод, который посылает случайный вопрос из случайного билета пользователю
    :param bot:
    :param update:
    :param user_data:
    """
    random_ticket = 1
    random_question = randint(1, 20)
    is_exam = 0
    button_info = str(random_ticket) + ';' + str(random_question) + ';' + str(is_exam)

    three_answers = [[
        InlineKeyboardButton(messages.ONE, callback_data='1;' + button_info),
        InlineKeyboardButton(messages.TWO, callback_data='2;' + button_info),
        InlineKeyboardButton(messages.THREE, callback_data='3;' + button_info)
    ]]

    four_answers = [[
        InlineKeyboardButton(messages.ONE, callback_data='1;' + button_info),
        InlineKeyboardButton(messages.TWO, callback_data='2;' + button_info),
        InlineKeyboardButton(messages.THREE, callback_data='3;' + button_info),
        InlineKeyboardButton(messages.FOUR, callback_data='4;' + button_info)
    ]]

    choices = db.get_number_of_choices(random_ticket, random_question)

    reply_markup = InlineKeyboardMarkup(three_answers) if int(choices) == 3 else InlineKeyboardMarkup(four_answers)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=db.get_question(random_ticket, random_question),
                    reply_markup=reply_markup)


def exam(bot, update, user_data):
    """
    Метод, который посылает подряд 20 вопросов одного билета, а в конце посылает результат экзамена
    :param bot:
    :param update:
    :param user_data:
    """
    random_ticket = 1
    question_number = 0
    write_answers = 0
    is_exam = 1
    button_info = str(random_ticket) + ';' + str(question_number) + ';' + str(is_exam) + ';' + str(write_answers)

    three_answers = [[
        InlineKeyboardButton(messages.ONE, callback_data='1;' + button_info),
        InlineKeyboardButton(messages.TWO, callback_data='2;' + button_info),
        InlineKeyboardButton(messages.THREE, callback_data='3;' + button_info)
    ]]

    four_answers = [[
        InlineKeyboardButton(messages.ONE, callback_data='1;' + button_info),
        InlineKeyboardButton(messages.TWO, callback_data='2;' + button_info),
        InlineKeyboardButton(messages.THREE, callback_data='3;' + button_info),
        InlineKeyboardButton(messages.FOUR, callback_data='4;' + button_info),
    ]]

    choices = db.get_number_of_choices(random_ticket, question_number)

    reply_markup = InlineKeyboardMarkup(three_answers) if int(choices) == 3 else InlineKeyboardMarkup(four_answers)

    bot.sendMessage(chat_id=update.message.chat_id,
                    text=messages.EXAM_STARTED + '\n' + db.get_question(random_ticket, question_number),
                    reply_markup=reply_markup)


def user_answer(bot, update):
    """
    Метод, определяет режим работы бота
    :param bot:
    :param update:
    """
    is_exam = int(update.callback_query.data.split(';')[3])

    if is_exam == 0:
        answer_for_training(bot, update)
    else:
        answer_for_exam(bot, update)


def answer_for_training(bot, update):
    """
    Метод отправляет пользователю случайный вопрос из случайного билета
    :param bot:
    :param update:
    """
    keyboard = [
        [InlineKeyboardButton(messages.NEXT, callback_data='5')],
        [InlineKeyboardButton(messages.MENU, callback_data='6')]
    ]

    query = update.callback_query
    user_choice = int(query.data.split(';')[0])
    ticket = int(query.data.split(';')[1])
    question = int(query.data.split(';')[2])
    comment = db.get_comment(ticket, question)
    write_choice = int(db.get_write_answer(ticket, question))

    if user_choice == 5:
        bot.sendMessage(chat_id=query.message.chat_id, text=db.get_question(ticket, question),
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    elif user_choice == 6:
        bot.sendMessage(chat_id=query.message.chat.id, text=messages.WELCOME)
    elif user_choice == write_choice:
        bot.sendMessage(chat_id=query.message.chat.id, text='Верно! \n\n' + comment,
                        message_id=query.message.message_id,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    else:
        bot.sendMessage(chat_id=query.message.chat.id, text='Неверно! \n\n' + comment,
                        message_id=query.message.message_id,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


def answer_for_exam(bot, update):
    """
    Метод посылает 20 вопросов пользователю, а в конце считает количество правильных ответов
    :param bot:
    :param update:
    """
    query = update.callback_query
    user_choice = int(query.data.split(';')[0])
    ticket = int(query.data.split(';')[1])
    question = int(query.data.split(';')[2])
    is_exam = int(update.callback_query.data.split(';')[3])
    write_answers = int(query.data.split(';')[4])
    print('write_answers BEFORE: ' + str(write_answers))

    if int(db.get_write_answer(ticket, question)) == int(user_choice):
        write_answers += 1

    question += 1
    print('write_answers AFTER: ' + str(write_answers))
    button_info = str(ticket) + ';' + str(question) + ';' + str(is_exam) + ';' + str(write_answers)
    print(button_info)

    if question < 20:
        print('next question ->')
        three_answers = [[
            InlineKeyboardButton(messages.ONE, callback_data='1;' + button_info),
            InlineKeyboardButton(messages.TWO, callback_data='2;' + button_info),
            InlineKeyboardButton(messages.THREE, callback_data='3;' + button_info)
        ]]

        four_answers = [[
            InlineKeyboardButton(messages.ONE, callback_data='1;' + button_info),
            InlineKeyboardButton(messages.TWO, callback_data='2;' + button_info),
            InlineKeyboardButton(messages.THREE, callback_data='3;' + button_info),
            InlineKeyboardButton(messages.FOUR, callback_data='4;' + button_info),
        ]]

        choices = db.get_number_of_choices(ticket, question)

        if int(choices) == 3:
            keyboard = InlineKeyboardMarkup(three_answers)
        else:
            keyboard = InlineKeyboardMarkup(four_answers)

        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                              text=db.get_question(ticket, question), reply_markup=keyboard)
    else:
        keyboard = [
            [InlineKeyboardButton(messages.MENU, callback_data='5')],
            [InlineKeyboardButton(messages.AGAIN, callback_data='6')],
        ]

        if 20 - int(write_answers) <= 2:
            result = messages.PASSED + str(write_answers)
        else:
            result = messages.FAILED + str(write_answers)

        bot.sendMessage(chat_id=query.message.chat.id,
                        text=result,
                        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))


if __name__ == '__main__':
    main()
