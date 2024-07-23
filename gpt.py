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
                "role": "assistant",
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

