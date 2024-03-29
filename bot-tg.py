import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from dflow_tools import query_dflow

import setup_logging


logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def send_message(bot, update):
    """Answer the user message via DialogFlow."""
    text = query_dflow(update.message.chat_id, update.message.text)
    if text is None:
        text = "Повторите Ваш вопрос"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    load_dotenv()
    setup_logging.config_logging(os.getenv("TELEGRAM_LOG_TOKEN"), os.getenv("TELEGRAM_LOG_CHAT_ID"))
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_TOKEN"))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - send the message via DialogFlow
    dp.add_handler(MessageHandler(Filters.text, send_message))

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
