import requests
import json


BASE_URL = 'http://18.236.132.102/games'

params = {
            "duration": 1000,
            "random": True,
            "board": ""
        }
resp = requests.post(BASE_URL, params=params)
content = json.loads(resp.content)
print(content)