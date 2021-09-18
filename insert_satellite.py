import requests
import json

filename = "C:\\Users\\Alan\\Documents\\django-project\\backend\\satellite_backend\\data\\active.txt"
line_number = 0;
min_line = 18;
max_line = 25;

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
        url = "http://127.0.0.1:8000/api/satellite-create/"
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(element), headers=headers)
        print(r.content)
       
