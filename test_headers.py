import requests

class TestHeaders:
    def test_headers(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_header')
        print(dict(response.headers))
        secret_header_value = response.headers.get('x-secret-homework-header')
        print(secret_header_value)

        assert secret_header_value == 'Some secret value', "The value of 'x-secret-homework-header' is not 'Some secret value'"