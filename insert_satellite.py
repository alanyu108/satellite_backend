import requests
import json

filename = "C:\\Users\\Alan\\Documents\\django-project\\backend\\satellite_backend\\data\\active.txt"
line_number = 0;
min_line = 0;
max_line = 22;

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

def parseTLE(obj):
    tle_1 = obj['tle_1']
    tle_2 = obj["tle_2"]
    
    #tle_1
    obj['norad'] = tle_1[2:7]
    obj['classification'] = tle_1[7]
    obj['international_designation'] = tle_1[9:15]
    obj['epoch_year'] = int("20" + tle_1[18:20])
    obj["epoch_day"] =float(tle_1[20:32])
    obj["first_derivative_mean_motion"] = float(tle_1[33:43])
    obj["second_derivative_mean_motion"] = float(tle_1[44:52][0] + '.' + tle_1[44:52][1:6] + 'e' + tle_1[44:52][6:8])
    obj["bstar"] =float(tle_1[53:61][0] + '.' + tle_1[53:61][1:6] + 'e' + tle_1[53:61][6:8])
    obj["set_number"] = int(tle_1[64:68])

    #tle_2
    obj["inclination"] =float(tle_2[8:16])
    obj["raan"] =float(tle_2[17:25])
    obj["eccentricity"] = float("0." + tle_2[26:33])
    obj["argp"] =float(tle_2[34:42])
    obj["mean_anomaly"] =float(tle_2[43:51])
    obj["mean_motion"] =float(tle_2[52:63])
    obj["rev_num"] =int(tle_2[63:68])
    return obj


for element in empty_list:
    if element:
        element["description"] = ""
        data = parseTLE(element)
        # print(data)
        url = "http://127.0.0.1:8000/api/satellite-create/"
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r)
       
