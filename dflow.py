import os
import requests


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
        json=payload
    )
    if response.ok:
        data = response.json()
        answer = data["result"]["speech"]
        return answer