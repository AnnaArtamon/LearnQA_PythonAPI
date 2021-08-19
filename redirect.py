import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
print(response.status_code)

history = response.history
number_of_redirects = len(history)
print(number_of_redirects)

print(history[number_of_redirects-1].url)
