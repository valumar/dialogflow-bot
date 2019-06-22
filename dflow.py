import os
import requests
import logging

logger = logging.getLogger(__name__)

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
        "timezone": "Europe/Moscow",
        "v": "20150910"
    }
    response = requests.post(
        f"{base_api_url}{api_command}",
        headers=headers,
        json=payload
    )
    logger.info(response.text)
    if response.ok:
        data = response.json()
        print(data)
        answer = data["result"]["fulfillment"]["speech"]
        if data["result"]["metadata"]["isFallbackIntent"]:
            answer = "Вам ответит оператор"
        return answer
