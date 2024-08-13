import requests
import config

def chat(text):
    prompt = {
        "modelUri": f"gpt://{config.KEY1}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f'ты эко-активист, хочешь что бы всё в мире было более экологичным. Не используй в ответе символы: "*"'
                # "text": f'ты эко-активист, хочешь что бы всё в мире было более экологичным, после ответа на вопрос пользователя ты делаешь несколько отступов и даёшь совет по экологии. Пользователь задал этот вопрос "{text}"'
            },
            {
                "role":"user",
                "text": text

            }

        ]
    }
    
    
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {config.KEY2}"
    }
    
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json().get('result')
    return result['alternatives'][0]['message']['text']

