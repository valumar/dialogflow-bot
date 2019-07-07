import random
import os
import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
from dflow_tools import query_dflow

import setup_logging


logger = logging.getLogger(__name__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=query_dflow(event.user_id, event.text),
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    load_dotenv()
    setup_logging.config_logging(os.getenv("TELEGRAM_LOG_TOKEN"), os.getenv("TELEGRAM_LOG_CHAT_ID"))
    vk_session = vk_api.VkApi(token=os.getenv("VK_GROUP_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
