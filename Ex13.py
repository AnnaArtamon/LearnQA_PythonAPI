import pytest
import requests
import json

user_agents = [
    ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"),
    ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1"),
    ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0"),
    ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
]

class TestUserAgent:
    @pytest.mark.parametrize('user_agent', user_agents)
    def test_user_agent(self, user_agent):
        headers = {'User-Agent': user_agent}
        response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check', headers=headers)
        response_json = json.loads(response.text)

        actual_platform = response.json()["platform"] #try to remember
        actual_browser = response_json['browser']
        actual_device = response_json['device']

        if user_agent == user_agents[0]:
            expected_platform = 'Mobile'
            expected_browser = 'No'
            expected_device = 'Android'
        elif user_agent == user_agents[1]:
            expected_platform = 'Mobile'
            expected_browser = 'Chrome'
            expected_device = 'iOS'
        elif user_agent == user_agents[2]:
            expected_platform = 'Googlebot'
            expected_browser = 'Unknown'
            expected_device = 'Unknown'
        elif user_agent == user_agents[3]:
            expected_platform = 'Web'
            expected_browser = 'Chrome'
            expected_device = 'No'
        elif user_agent == user_agents[4]:
            expected_platform = 'Mobile'
            expected_browser = 'No'
            expected_device = 'iPhone'

        assert actual_platform == expected_platform, f'Platform "{actual_platform}" is not what we expected'
        assert actual_browser == expected_browser, f'Browser "{actual_browser}" is not what we expected'
        assert actual_device == expected_device, f'Device "{actual_device}" is not what we expected'

