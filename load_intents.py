import logging
import os
import requests

from dotenv import load_dotenv


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def download_phrases():
    url = "https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.ok:
            return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTPError: {e}')

def post_intent(data):
    baseurl = "https://api.dialogflow.com/v1/"
    api_command = "intents"
    access_token = os.getenv("DIALOGFLOW_DEV_TOKEN")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(
        f"{baseurl}{api_command}",
        headers=headers,
        json=data
    )
    if response.ok:
        return response.json()


def main():
    load_dotenv()
    phrases = download_phrases()
    for phrase in phrases:
        name = phrase
        speech = phrases[phrase]['answer']

        template = {
            "name": name,
            "auto": True,
            "responses": [
                {
                    "speech": speech
                }
            ],
            "userSays": []
        }

        for question in phrases[phrase]['questions']:
            user_says_data = {
                "data": [
                    {
                        "text": question
                    }
                ]
            }
            template['userSays'].append(user_says_data)
        logger.info(post_intent(template))


if __name__ == '__main__':
    main()



