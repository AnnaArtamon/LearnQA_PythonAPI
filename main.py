import requests

print("Hello from Anna")

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)