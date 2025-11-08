from pprint import pprint
from dotenv import load_dotenv
import requests
import os
import logging

# Загружаем переменные из .env файла
load_dotenv()

api_key = os.getenv("API_KEY")
ai_model = "mistralai/Magistral-Small-2506"

logging.basicConfig(level=logging.INFO)

def make_request(message_text):
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    data = {
        "model": ai_model,
        "messages": [
            {
                "role": "system",
                "content": "Ты универсальный помощник.",
            },
            {
                "role": "user",
                "content": message_text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    # Извлекаем только текст ответа
    if 'choices' in data and len(data['choices']) > 0:
        return data['choices'][0]['message']['content']
    else:
        return data


def main():
    result = make_request("Привет! Напиши только 1 или 0 и больше ничего, если Python - это язык, то 1, иначе 0")
    pprint(result)


if __name__ == "__main__":
    main()