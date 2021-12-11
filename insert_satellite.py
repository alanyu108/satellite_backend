import requests
import json
from satellite_api.functions import parseTLE

filename = "C:\\Users\\Alan\\Documents\\django-project\\backend\\satellite_backend\\data\\debris-cosmos.txt"
line_number = 0;
min_line = 0; #not inclusive
max_line = 31; #not inclusive

empty = {}
empty_list = list([]);
with open(filename, "r") as f:
    for line in f.readlines():
        if line_number < max_line and line_number >= min_line:
            line = line.rstrip()
            if line_number % 3 == 0:
                empty_list.append(empty)
                empty = {};
                empty["name"] = line
            elif line_number % 3 == 1:
                empty["tle_1"] = line
            elif line_number % 3 == 2:
                empty["tle_2"] = line    
        line_number += 1;

for element in empty_list:
    if element:
        # element["description"] = ""
        data = parseTLE(element)
     
        url = "http://127.0.0.1:8000/api/debris/create/"
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(element), headers=headers)
        print(r.status_code)
       
