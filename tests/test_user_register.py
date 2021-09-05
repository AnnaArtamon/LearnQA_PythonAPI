import allure

from lib.assertions import Assertions
from lib.base_case import BaseCase
import pytest
from lib.my_requests import MyRequests


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    exclude_params = ["username", "firstName", "lastName",
                "email", "password"]

    @allure.description("This test tries to create a user with an email that has already been registered")
    def test_create_existing_user(self):
        email = "vinkotov@example.com"
        data = self.prepare_reg_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"Users with email '{email}' already exists")

    @allure.description("Positive test of creating new user")
    def test_create_new_user(self):

        data = self.prepare_reg_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test tries to create a user with an email with invalid format")
    def test_create_user_no_at(self):
        data = self.prepare_reg_data("invalid")
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, "Invalid email format")

    @allure.description("This test tries to create a user without some obligatory info")
    @pytest.mark.parametrize('excluded_param', exclude_params)
    def test_create_user_wo_oblig_info(self, excluded_param):
        data = self.prepare_reg_data()
        del data[excluded_param]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {excluded_param}", \
            f"Unexpected response content {response.content}"

    @allure.description("This test tries to create a user with a username consisting of one symbol")
    def test_create_user_short_name(self):
        username = "a"
        data = self.prepare_reg_data()
        data.update(username = username)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The value of 'username' field is too short")

    @allure.description("This test tries to create a user with a username consisting of 251 symbol")
    def test_create_user_long_name(self):
        username = ''.join(['a' for i in range(251)])
        data = self.prepare_reg_data()
        data.update(username=username)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_content(response, f"The value of 'username' field is too long")

