from time import sleep

import allure
import pytest
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


@allure.epic("Editing user's info cases")
class TestUserEdit(BaseCase):
    auth_conditions = [("no_token"), ("no_cookie"), ("no_both")]

    def setup(self):
        # CREATE
        reg_data = self.prepare_reg_data()
        response1 = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        self.email = reg_data["email"]
        self.password = reg_data["password"]
        self.user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {"email": self.email, "password": self.password}
        response2 = MyRequests.post("/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")


    @allure.description("Positive test of editing user's info")
    def test_edit_just_created_user(self):
        # EDIT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"firstName": new_name})
        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})
        first_name_after_edit = self.get_json_value(response4, "firstName")

        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_key(response4, "firstName", first_name_after_edit, "Name hasn't changed")

    @allure.description("This test checks inability to edit user's info while unauthorized")
    @pytest.mark.parametrize('condition', auth_conditions)
    def test_edit_not_auth(self, condition):
        # EDIT
        new_name = "Changed name"
        if condition == "no_token":
            response3 = MyRequests.put(f"/user/{self.user_id}",
                                     cookies={"auth_sid": self.auth_sid},
                                     data={"firstName": new_name})
        elif condition == "no_cookie":
            response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 data={"firstName": new_name})
        elif condition == "no_both":
            response3 = MyRequests.put(f"/user/{self.user_id}",
                                     data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_content(response3, "Auth token not supplied")

    @allure.description("This test checks inability to edit another user's info while authorized")
    def test_edit_another_user(self):
        #CREATE ANOTHER USER
        reg_data = self.prepare_reg_data()
        response1 = MyRequests.post("/user/", data=reg_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        another_user_id = self.get_json_value(response1, "id")
        another_user_email = reg_data["email"]
        another_user_password = reg_data["password"]
        another_user_first_name = reg_data["firstName"]

        # EDIT ATTEMPT
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{another_user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"firstName": new_name})

        # LOGIN ANOTHER USER
        login_data = {"email": another_user_email, "password": another_user_password}
        response2 = MyRequests.post("/user/login", data=login_data)
        another_auth_sid = self.get_cookie(response2, "auth_sid")
        another_token = self.get_header(response2, "x-csrf-token")

        # GET ANOTHER USER INFO
        response4 = MyRequests.get(f"/user/{another_user_id}",
                                 headers={"x-csrf-token": another_token},
                                 cookies={"auth_sid": another_auth_sid})
        first_name_after_edit_attempt = self.get_json_value(response4, "firstName")
        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_key(response4, "firstName", another_user_first_name,
                                            f"Another user name has changed, it's {first_name_after_edit_attempt}")

    @allure.description("This test tries to change user's email to one with invalid format")
    def test_edit_wrong_email(self):
        # EDIT ATTEMPT
        new_email = self.prepare_invalid_email()
        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"email": new_email})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_response_content(response3, "Invalid email format")

        # GET
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})
        email_after_edit_attempt = self.get_json_value(response4, "email")

        Assertions.assert_json_value_by_key(response4, "email", self.email,
                                            f"Email value has changed, it's {email_after_edit_attempt} now")

    @allure.description("This test tries to change user's first name to a one-symbol name")
    def test_edit_short_name(self):
        # EDIT
        new_short_name = "a"
        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid},
                                 data={"firstName": new_short_name})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_key(response3, "error", "Too short value for field firstName",
                                            f"The error message is not what we expected")

        # GET
        response4 = MyRequests.get(f"/user/{self.user_id}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})
        first_name_after_edit_attempt = self.get_json_value(response4, "firstName")

        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_key(response4, "firstName", first_name_after_edit_attempt, "Name has changed to a short name")





