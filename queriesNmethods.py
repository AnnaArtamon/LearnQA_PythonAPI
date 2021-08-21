import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

response_no_params = requests.get(url)
print(response_no_params.status_code)
print(response_no_params.text)

response_head = requests.head(url)
print(response_head.status_code)
print(response_head.text)

ok_response = requests.get(url, params={"method": "GET"})
print(ok_response.status_code)
print(ok_response.text)

for method in 'GET', 'POST', 'PUT', "DELETE", 'HEAD', 'PATCH', 'OPTIONS', 'CONNECT', 'TRACE':
    print(method)
    print('get  ', requests.get(url, params={"method": f'{method}'}).text)
    print('post', requests.post(url, data={"method": f'{method}'}).text)
    print('put', requests.put(url, data={"method": f'{method}'}).text)
    print('delete', requests.delete(url, data={"method": f'{method}'}).text)
    print('---')
