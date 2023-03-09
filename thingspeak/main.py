import json
import traceback
import sys
import os
import pickle

import lumen

import requests
from datetime import datetime

try:
    __location__ =  os.getenv('PERSISTENT_DATA_PATH', default = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))) # Get persistent data storage location
    previous_download_log = 'output.pkl'
    if os.path.exists(os.path.join(__location__, previous_download_log)):
        with open(os.path.join(__location__, previous_download_log),'rb') as f:
            previous_result = pickle.load(f)
    else:
        previous_result = ""

    result = requests.get(url="https://api.thingspeak.com/channels/2011025/feeds.json?results=1")
    json_data = result.json()
    temperature_data = json_data["feeds"][0]["field1"]
    parse_data = temperature_data.split(",-")[0]
    parse_data = parse_data.replace("'", '"')
    parse_data = parse_data.replace(" ", '')
    parse_data = "[" + parse_data + "]"

    json_temp = json.loads(parse_data)
    
    date_time = json_data["feeds"][0]["created_at"]
    starting_epoch = int(datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()) - (3*60)

    results = []
    for item in json_temp:
        temp = {}
        temp["arduino_time"] = list(item.keys())[0]
        temp["temperature"] = item[list(item.keys())[0]]
        temp["date_time"] = date_time
        temp["epoch"] = starting_epoch
        results.append(temp)
        starting_epoch = starting_epoch + 15

    output = {"results": results}

    if previous_result == json_temp: # we have already received this
        lumen.save_exception( f"Data already received")
        sys.exit(1)
    else:
        with open(os.path.join(__location__, previous_download_log), 'wb') as f:
            pickle.dump(json_temp, f)
        lumen.save(output)

except Exception as e:
    lumen.save_exception(traceback.format_exc())