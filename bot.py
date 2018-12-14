# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import messages

TOKEN = '569532381:AAH5Ujv0o3pMLQsv-iHXNjHD0npmWElwztE'
PORT = '5001'
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format=messages.LOGGING, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(TOKEN, request_kwargs=PROXY)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://pdd-exam-bot.herokuapp.com//" + TOKEN)
    updater.idle()


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


if __name__ == '__main__':
    main()
