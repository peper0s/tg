import json
import time
import config
import base64
from PIL import Image
from io import BytesIO

import requests

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def save(self, base_image, file):
        data = base64.b64decode(base_image)
        image = Image.open(BytesIO(data))
        image.save(file)


def create_image(text):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', config.KEY4, config.KEY3)
    model_id = api.get_model()
    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)
    api.save(images[0],'test.png')


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', config.KEY4, config.KEY3)
    model_id = api.get_model()
    uuid = api.generate('python', model_id)
    images = api.check_generation(uuid)
    api.save(images[0],'test.png')