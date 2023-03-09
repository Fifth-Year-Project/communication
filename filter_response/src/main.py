import traceback
import sys
import json

import lumen

import requests
import datetime

def poll_temp_sensors():
    headers = {'Content-Type': 'application/x-www-form-urlencoded',}
    data = '{"access_key": "5bdd8b2f-fa79-4620-8dfe-9c91becf87f2", "limit": 1}'
    response = requests.post('https://sdls.lumen.live/documents/external/filter', headers=headers, data=data)
    temperature_info = response.json()[0]["execution-results"]["results"]
    return(temperature_info)

try:
    temperature_data = json.loads(sys.argv[2])
    #temperature_data = poll_temp_sensors()
    sum = 0
    for temperature_reading in temperature_data:
        temperature_value = temperature_reading["temperature"]
        sum += temperature_value
        epoch = temperature_reading["epoch"]*1000
    average = sum/len(temperature_data)

    if 100 < average < -30:
        lumen.save_exception("Erroneous data")

    lumen.save({"average_temperature": average,
                "epoch": epoch})
except:
    lumen.save_exception(traceback.format_exc())
