import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestAuth(BaseCase):
    exclude_params = [("no_cookie"),
                      ("no_token")]

    def setup(self):
        data = {'email': 'vinkotov@example.com', 'password': '1234'}
        response = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        self.cookie_auth_sid = self.get_cookie(response, "auth_sid")
        self.header_token = self.get_header(response, "x-csrf-token")
        self.user_id_auth = self.get_json_value(response, "user_id")

    def test_auth(self):
        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 headers={"x-csrf-token": self.header_token},
                                 cookies={"auth_sid": self.cookie_auth_sid})

        Assertions.assert_json_value_by_key(response2, "user_id", self.user_id_auth,
                                             "User_id from check method is not equal to user_id form auth method")

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth(self, condition):

        if condition == "no_cookie":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     headers={"x-csrf-token": self.header_token})
        elif condition == "no_token":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     cookies={"auth_sid": self.cookie_auth_sid})

        Assertions.assert_json_value_by_key(response2, "user_id", 0,
                                             f"User is authorized with condition {condition}")
