from requests import Response
import json

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, key_name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. The response text is '{response.text}'"
        assert key_name in response_as_dict, f"There's no key '{key_name}' in the response"
        assert expected_value == response_as_dict[key_name], error_message
