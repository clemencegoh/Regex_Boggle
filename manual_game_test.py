import requests
import json


BASE_URL = "http://localhost:5000/games"

params = {
            "duration": 1000,
            "random": True,
            "board": ""
        }
resp = requests.post(BASE_URL, json=params)
content = json.loads(resp.content)
print(content)


# params = {
#     "token": '2b1a32abec348262fe6f5b18442573e520dc028128efddab2d05f9ef5b706c71',
#     "id": 1,
#     "word": "POP"
# }
# resp = requests.put(BASE_URL + '/1', json=params)
# content = json.loads(resp.content)
# print(content)

# TAP*
# EAKS
# HMSW
# SMHI