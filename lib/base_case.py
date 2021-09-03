from datetime import datetime
import json
from requests import Response


class BaseCase:
    constant_part = "someemail"
    domain = "mail.ru"

    def get_variable_part(self):
        return datetime.now().strftime("%d%m%Y%H%M%S")

    def prepare_email(self):
        email = f"{self.constant_part}{self.get_variable_part()}@{self.domain}"
        return email

    def prepare_invalid_email(self):
        email = f"{self.constant_part}{self.get_variable_part()}{self.domain}"
        return email

    def prepare_reg_data(self, email=None):
        if email is None:
            email = self.prepare_email()
        elif email == "invalid":
            email = self.prepare_invalid_email()

        reg_data = {"username": "username", "firstName": "firstName", "lastName": "lastName",
                "email": email, "password": "password"}
        return reg_data

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can't find cookie named '{cookie_name}' in the response"
        return response.cookies.get(cookie_name)

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Can't find header named '{header_name}' in the response"
        return response.headers[header_name]

    def get_json_value(self, response: Response, key_name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. The response text is '{response.text}'"
        assert key_name in response_as_dict, f"Response JSON doesn't have key '{key_name}'"
        return response_as_dict[key_name]