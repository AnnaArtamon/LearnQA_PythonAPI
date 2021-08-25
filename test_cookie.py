import requests


class TestCookie:
    def test_cookie(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        dict_cookies = dict(response.cookies)
        print(dict_cookies)
        for key in dict_cookies:
            cookie_name = key
        print(cookie_name)
        cookie_value = response.cookies.get('HomeWork')
        print(cookie_value)

        assert cookie_name == 'HomeWork', "Cookie name is not 'HomeWork'"
        assert cookie_value == 'hw_value', "Wrong cookie value"
