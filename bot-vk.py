import random
import os

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv


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
        "sessionId": str(session_id),
        "timezone": "Europe/Moscow"
    }

    response = requests.post(
        f"{base_api_url}{api_command}",
        headers=headers,
        json=payload,
    )
    print(response.url, response.text)
    if response.ok:
        data = response.json()
        print(data)
        answer = data["result"]["speech"]
        if data["result"]["metadata"]["isFallbackIntent"]:
            answer = "Вам ответит оператор"
        return answer



def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=query_dflow(event.user_id, event.text),
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    load_dotenv()
    vk_session = vk_api.VkApi(token=os.getenv("VK_GROUP_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)