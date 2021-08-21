import requests

print("Hello from Anna")

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)

payload = {"name": "User"}

response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response.text)

