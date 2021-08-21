import json
import requests
import time


response = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job')
resp_json = json.loads(response.text)
token = resp_json["token"]
seconds = resp_json["seconds"]

response1 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
resp1_json = json.loads(response1.text)
print(resp1_json['status'])

time.sleep(seconds)
response2 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job', params={'token': token})
resp2_json = json.loads(response2.text)
print(resp2_json['status'])
print(resp2_json['result'])


