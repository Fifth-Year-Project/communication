import requests
import json


result = requests.get(url="https://api.thingspeak.com/channels/2011025/feeds.json?results=1")
json_data = result.json()
temperature_data = json_data["feeds"][0]["field1"]
parse_data = temperature_data.split(",-")[0]
parse_data = parse_data.replace("'", '"')
parse_data = parse_data.replace(" ", '')
json_temp = json.loads(parse_data)
a=1