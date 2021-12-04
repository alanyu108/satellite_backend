import requests
import json

satellite_url = "http://127.0.0.1:8000/api/satellites/"
satellite_visible_url = "http://127.0.0.1:8000/api/satellite-visible/"

satellite_get = requests.get(url=satellite_url)
satellite_name = [x['name'] for x in satellite_get.json()]
longlatalt = [ 40.7128, 74.0060, 24]

satellite_obj = [
                {"name": x, 
                "longitude": longlatalt[0],
                 "latitude": longlatalt[1], 
                 "altitude": longlatalt[2]} for x in satellite_name]

for satellite in satellite_obj:
    headers = {'Content-type': 'application/json'}
    r = requests.post(satellite_visible_url, data=json.dumps(satellite), headers=headers)
    if r.status_code == 200:
        satellite_visible = r.json()
        if 'message' in satellite_visible:
            print({"name": satellite['name'], "message": satellite_visible['message']})
        else:
            print(satellite_visible)
