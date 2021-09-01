from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_key(response: Response, key, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. The response text is '{response.text}'"
        assert key in response_as_dict, f"There's no key '{key}' in the response"
        assert response_as_dict[key] == expected_value, error_message

    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Status code is not {expected_status_code}, " \
                                                             f"it's {response.status_code}"

    @staticmethod
    def assert_json_has_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. The response text is '{response.text}'"
        assert key in response_as_dict, f"There's no key '{key}' in the response"

    @staticmethod
    def assert_json_has_no_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. The response text is '{response.text}'"
        assert key not in response_as_dict, f"There's key '{key}' in the response although not expected"

    @staticmethod
    def assert_response_content(response: Response, expected_content):
        assert response.content.decode("utf-8") == expected_content, f"Unexpected response content"