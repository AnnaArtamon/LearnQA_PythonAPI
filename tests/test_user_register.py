from datetime import datetime
import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase
import pytest


class TestUserRegister(BaseCase):
    exclude_params = [("no_username"), ("no_firstName"), ("no_lastName"),
                ("no_email"), ("no_password")]

    def setup(self):
        self.constant_part = "someemail"
        self.variable_part = datetime.now().strftime("%d%m%E%H%M%S")
        self.domain = "mail.ru"
        self.email = f"{self.constant_part}{self.variable_part}@{self.domain}"

    def test_create_existing_user(self):
        email = "vinkotov@example.com"
        data = {"username": "username", "firstName": "firstName", "lastName": "lastName",
                "email": email, "password": "password"}
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")


    def test_create_new_user(self):

        data = {"username": "username", "firstName": "firstName", "lastName": "lastName",
                "email": self.email, "password": "password"}
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_no_at(self):
        email = f"{self.constant_part}{self.variable_part}{self.domain}"
        data = {"username": "username", "firstName": "firstName", "lastName": "lastName",
                "email": email, "password": "password"}

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_wo_oblig_info(self, condition):

        if condition == "no_username":
            data = {"firstName": "firstName", "lastName": "lastName",
                "email": self.email, "password": "password"}
            excluded_param = "username"
        elif condition == "no_firstName":
            data = data = {"username": "username", "lastName": "lastName",
                "email": self.email, "password": "password"}
            excluded_param = "firstName"
        elif condition == "no_lastName":
            data = {"username": "username", "firstName": "firstName",
                "email": self.email, "password": "password"}
            excluded_param = "lastName"
        elif condition == "no_email":
            data = {"username": "username", "firstName": "firstName",
                    "lastName": "lastName", "password": "password"}
            excluded_param = "email"
        elif condition == "no_password":
            data = {"username": "username", "firstName": "firstName",
                    "lastName": "lastName", "email": self.email}
            excluded_param = "password"

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {excluded_param}", \
                                                    f"Unexpected response content {response.content}"

    def test_create_user_short_name(self):
        username = "a"
        data = {"username": username, "firstName": "firstName", "lastName": "lastName",
                "email": self.email, "password": "password"}
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The value of 'username' field is too short")

    def test_create_user_long_name(self):
        username = ''.join(['a' for i in range(251)])
        data = {"username": username, "firstName": "firstName", "lastName": "lastName",
                "email": self.email, "password": "password"}
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The value of 'username' field is too long")

