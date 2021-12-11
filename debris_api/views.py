from rest_framework.response import Response
from rest_framework.decorators import api_view
from debris.models import Debris
from debris_api.functions import parseTLE
from debris_api.serializers import DebrisSerializer
import json

# Create your views here.

@api_view(['POST'])
def debrisDetail(request):
    try: 
        user_request = request.data

        if 'norad' in user_request:
            norad = user_request['norad']
            debris = Debris.objects.get(norad=norad);
            serializer = DebrisSerializer(debris, many=False);
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "body must contain norad key"}, status = 400)
    except Debris.DoesNotExist:
        return Response(data={'message':'Could not find debris'}, status=404)


@api_view(['GET'])
def debrisList(_):
    debris = Debris.objects.all();
    serializer = DebrisSerializer(debris, many=True);
    return Response(serializer.data, status=200)



@api_view(['POST'])
def debrisCreate(request):
    allowed = ["name", "tle_1", "tle_2"]
    allow_to_change = True
    for value in allowed:
        if value not in request.data:
             allow_to_change = False
    if allow_to_change:
        parsed_data = parseTLE(request.data)
        serializer = DebrisSerializer(data=parsed_data);
        if serializer.is_valid():
            serializer.save()
            return Response(parsed_data)
        return Response({"message": "Unable to insert data into database", "error": serializer.errors}, status=400)
    else:
         return Response({"message": "Unable to create debris", "error": "data must contains the keys name, tle_1, tle_2"}, 400)

@api_view(['PUT'])
def debrisUpdate(request):
    allowed = ["name", "tle_1", "tle_2", 'norad'] #data the user is allowed to change
    allow_to_change = True
    for value in allowed:
        if value not in request.data:
             allow_to_change = False
    
    if  allow_to_change :
        user_request = request.data
        if 'norad' in user_request:
            norad = user_request['norad']
            parsed_data = parseTLE(request.data)
            parsed_data['name'] = user_request['name']
            debris = Debris.objects.get(norad=norad);
            serializer = DebrisSerializer(instance=debris, data=parsed_data);

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({"message": "Unable to update debris", "errors": serializer.errors}, status=405)
        else:
            return Response({"message": "body must contain norad key"}, status = 400)
    return Response({"message": "Unable to update debris", "error": "data must contains the keys name, tle_1, tle_2 and norad"}, 400)

@api_view(['DELETE'])
def debrisDelete(request):
    try: 
        user_request = request.data
        if 'norad' in user_request:
            norad = user_request['norad']
            debris = Debris.objects.get(norad=norad);
            debris.delete();
            return Response(data={'message': 'item has been deleted'}, status=200)
        else:
            return Response({"message": "body must contain norad key"}, status = 400)
    except Debris.DoesNotExist:
        return Response(data={'message': 'item was not found'}, status=404)
    

@api_view(['POST'])
def debrisSearch(request):
    user_request = request.data
    if 'search' in user_request:
        search_value = user_request['search'].strip()

        if not search_value == "":
            satellites = Debris.objects.all();
            serializer = DebrisSerializer(satellites, many=True);

            data = json.loads(json.dumps(serializer.data))
            filtered_satellites = [x for x in data if x['name'].find(search_value) != -1]

            if len(filtered_satellites) != 0: 
                return Response(data=filtered_satellites, status=200)
            else:
                return Response(data={"message": "no item was found"}, status=404)
        else:
            return Response(data={"message": "search key must have a corresponding value"}, status=400)
    else:
        return Response(data={"message": "body must contain search key"}, status=400)

@api_view(['GET'])
def debrisPage(_, number):
    if isinstance(number, int) and number >= 1:
        debris = Debris.objects.all();
        serializer = DebrisSerializer(debris, many=True);
        
        debris_num = 5
        page_num = number
        iter = debris_num * (page_num - 1)
        filtered_debris = []

        for i in range(iter, iter + debris_num):
            if i < len(serializer.data):
                filtered_debris.append(serializer.data[i])
            else:
                break;
        return Response(filtered_debris, status=200)
    else:
        return Response(data={'message':'page number must be an integer'}, status=400)
   

@api_view(['GET'])
def debrisOverview(_):
    data = {
        'message': 'This is the debris overivew api route',
        'routes': 
        {
            "all/": {
                'request-type': 'GET',
                'description': "returns all debris in the database",
                'example': "/api/debris/all", 
            },
            "page=<int>/": {
                'request-type': 'GET',
                "description":"returns a limited amount of debris based on the page number , default is 5, int must be greater than or equal to 1",
                'example': "/api/debris/page=1/", 
            },
            "search/": {
                'request-type': 'POST',
                'description': "returns all debris in the database given a search key and value, search uses the debris' name, to find debris with norad id use /api/debris/ route",
                'content-type':'application/json',
                'example': "/api/debris/search/", 
                'request body': {
                    'search': "ca"
                },
            },
            "": {
                'request-type': 'POST',
                'description': "returns a satellite in the database given its norad id",
                'example': "/api/debris/",
                'content-type':'application/json',
                'request body': {
                    'norad': "33764"
                }, 
            },
            "create/": {
                'request-type': 'POST',
                'description': "adds a new debris entry into the database, data sent to this route must have the keys name, tle_1, tle_2 ",
                'example': "/api/debris/create/", 
                'request body': {
                    "name": "COSMOS 2251 DEB",
                    "tle_1": "1 33764U 93036M   21345.55631112  .00000166  00000+0  66634-4 0  9994",
                    "tle_2": "2 33764  74.0362  81.7831 0024183  39.0588 330.9424 14.35364036671538",
                }
            },
            "update/": {
                'request-type': 'PUT',
                'description': "updates a debris given its name,  data sent to this route must have the keys: name, tle_1, tle_2 and norad id used as an identifier",
                'example': "/api/satellite-update/",
                'content-type':'application/json', 
                'request body': {
                    "norad": 33764,
                    "name": "COSMOS 2251 DEB",
                    "tle_1": "1 33764U 93036M   21345.55631112  .00000166  00000+0  66634-4 0  9994",
                    "tle_2": "2 33764  74.0362  81.7831 0024183  39.0588 330.9424 14.35364036671538",
                }
            },
            "delete/": {
                'request-type': 'DELETE',
                'description': "delete a debris given its norad id",
                'content-type':'application/json',
                'example': "/api/satellite-delete/",
                'request body': {
                    "norad": 33764,
                },
            },
        }
    }
    return Response(data=data)
   

