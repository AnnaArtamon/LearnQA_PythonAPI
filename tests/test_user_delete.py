import time
import pytest

import allure
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("User deletion cases")
class TestUserDelete(BaseCase):
    def setup(self):
        #CREATE
        reg_data = self.prepare_reg_data()
        response1 = MyRequests.post("/user/", data=reg_data)
        self.user_id = response1.json()["id"]
        self.email = reg_data["email"]
        self.password = reg_data["password"]

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # LOGIN
        login_data = {"email": self.email, "password": self.password}
        response2 = MyRequests.post("/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

    @pytest.mark.skip(reason="will do it tomorrow")
    @allure.description("This test tries to delete the user which is prohibited to delete")
    def test_delete_undeletable_user(self):
        #LOGIN
        login_data = {'email': 'vinkotov@example.com', 'password': '1234'}
        user_id = 2
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_status_code(response2, 200)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #DELETE
        ressponse5 = MyRequests.delete(f"/user/{user_id}", headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(ressponse5, 400)
        Assertions.assert_response_content(ressponse5, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("Positive test of deleting a user")
    def test_delete_user(self):
        #DELETE
        ressponse5 = MyRequests.delete(f"/user/{self.user_id}", headers={"x-csrf-token": self.token},
                                       cookies={"auth_sid": self.auth_sid})
        Assertions.assert_status_code(ressponse5, 200)

        #GET ATTEMPT
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})
        Assertions.assert_status_code(response4, 404)
        Assertions.assert_response_content(response4, "User not found")

    @allure.description("This test tries to delete another user")
    def test_delete_another_user(self):
        # CREATE ANOTHER USER
        reg_data = self.prepare_reg_data()
        response1 = MyRequests.post("/user/", data=reg_data)

        print(response1.content)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        another_user_id = self.get_json_value(response1, "id")

        # DELETE ATTEMPT
        response5 = MyRequests.delete(f"/user/{another_user_id}", headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})

        # GET ANOTHER USER INFO
        response4 = MyRequests.get(f"/user/{another_user_id}")

        Assertions.assert_json_has_key(response4, "username")
