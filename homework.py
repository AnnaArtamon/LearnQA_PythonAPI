import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is the second message","timestamp":"2021-06-04 16:41:01"}]}'

json = json.loads(json_text)
print(json["messages"][1]["message"])