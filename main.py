import logging
import os
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def send_message(bot, update):
    """Answer the user message via DialogFlow."""
    bot.send_message(
        chat_id=update.message.chat_id,
        text=query_dflow(update.message.chat_id, update.message.text),
    )


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def query_dflow(session_id, query):
    access_token = os.getenv("DIALOGFLOW_DEV_TOKEN")
    base_api_url = "https://api.dialogflow.com/v1/"
    api_command = "query"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "lang": "ru",
        "query": query,
        "sessionId": session_id,
        "timezone": "Europe/Moscow"
    }
    response = requests.post(
        f"{base_api_url}{api_command}",
        headers=headers,
        json=payload
    )
    if response.ok:
        data = response.json()
        answer = data["result"]["speech"]
        return answer


def main():
    load_dotenv()
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
    # print(query_dflow("1111", "Привет, железка"))
