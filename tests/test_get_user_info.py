import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestGetUserInfo(BaseCase):
    def setup(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.cookie_auth_sid = self.get_cookie(response, "auth_sid")
        self.header_token = self.get_header(response, "x-csrf-token")
        self.user_id_auth = self.get_json_value(response, "user_id")

    def test_get_user_info_unauth(self):
        id = 2
        unexpected_keys = ["id", "email", "firstName", "lastName"]
        response = requests.get(f"https://playground.learnqa.ru/api/user/{id}")
        Assertions.assert_json_has_key(response, "username")
        for key in unexpected_keys:
            Assertions.assert_json_has_no_key(response, key)

    def test_get_user_info_auth(self):
        expected_keys = ["id", "username", "email", "firstName", "lastName"]
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{self.user_id_auth}",
                                 cookies={"auth_sid": self.cookie_auth_sid}, headers={"x-csrf-token": self.header_token})
        for key in expected_keys:
            Assertions.assert_json_has_key(response2, key)

    def test_get_another_user_info(self):
        another_user_id = "8654"
        unexpected_keys = ["id", "email", "firstName", "lastName"]
        response2 = requests.get(f"https://playground.learnqa.ru/api/user/{another_user_id}",
                                 cookies={"auth_sid": self.cookie_auth_sid},
                                 headers={"x-csrf-token": self.header_token})
        Assertions.assert_json_has_key(response2, "username")
        for key in unexpected_keys:
            Assertions.assert_json_has_no_key(response2, key)

