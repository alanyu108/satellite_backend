import json
import logging
from urllib.parse import parse_qs
from api.functions import parseTLE
from satellite.models import Satellite
from satellite.models import Satellite
from .serializers import SatelliteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


logger = logging.getLogger("mylogger")
#logger.info() print to command line

# Create your views here.
@api_view(['GET'])
def apiOverview(_):
    data = {
        'message': 'This is the satellite api route',
        'routes': {
            "satellites/": {
                'request-type': 'GET',
                'description': "returns all satellites in the database",
                'example': "/api/satellites/", 
            },
            "satellites/:query": {
                'request-type': 'GET',
                'description': "returns all satellites in the database based on given query",
                'query': {
                    "page": {
                        "description":"returns a limited amount of satellites based on the page number , default is 5",
                        'example': "/api/satellites/page=1/", 
                    }, 
                    "search": {
                        "description":"returns satellites based on search parameter",
                        'content-type':'application/json',
                        'example': "/api/satellites/search/", 
                        'request body': {
                            'search': "ca"
                        },
                    }, 
                },
            },
            "satellite/": {
                'request-type': 'GET',
                'description': "returns a satellite in the database given its name",
                'example': "/api/satellite/",
                'content-type':'application/json',
                'request body': {
                    'name': "CALSPHERE 1"
                }, 
            },
            "satellite-create/": {
                'request-type': 'POST',
                'description': "adds a new satellite entry into the database, data sent to this route must have the keys name, tle_1, tle_2 and description",
                'example': "/api/satellite-create/", 
            },
             "satellite-update/": {
                'request-type': 'PUT',
                'description': "updates a satellite given its name,  data sent to this route must have the keys: name, tle_1, tle_2 and description",
                'example': "/api/satellite-update/",
                'content-type':'application/json', 
                'request body': {
                    "name": "LCS 1",
                    "tle_1": "1 01361U 65034C   21260.47481222  .00000019  00000-0  13880-2 0  9992",
                    "tle_2": "2 01361  32.1454 333.4385 0012647 350.6526   9.3735  9.89299852 38197",
                    "description": "test"
                }
                
            },
             "satellite-delete/": {
                'request-type': 'DELETE',
                'description': "delete a satellite given its name",
                'content-type':'application/json',
                'example': "/api/satellite-delete/",
                'request body': {
                    "name": "CALSPHERE 1",
                },
            },
        }
    }
    return Response(data=data)

@api_view(['GET'])
def satelliteList(_):
    try: 
        satellites = Satellite.objects.all();
        serializer = SatelliteSerializer(satellites, many=True);
        return Response(serializer.data, status=200)
    except Satellite.DoesNotExist:
        return Response(data={'message':'There are no satellites data in the database'}, status=404)


@api_view(['GET'])
def satelliteQuery(request, query):
    try: 
        parsed_query = parse_qs(query)
        if 'page' in parsed_query: 
            if isinstance(int(parsed_query['page'][0]), int) and int(parsed_query['page'][0]) >= 1 :
                satellites = Satellite.objects.all();
                serializer = SatelliteSerializer(satellites, many=True);
                
                satellite_num = 5
                page_num = int(parsed_query['page'][0])
                iter = satellite_num * (page_num - 1)
                filtered_satellite = []

                for i in range(iter, iter + satellite_num):
                    if i < len(serializer.data):
                        filtered_satellite.append(serializer.data[i])
                    else:
                        break;
                return Response(filtered_satellite, status=200)
            else:
                return Response(data={'message':'page number must be an integer'}, status=400)
        elif 'search' == query:
            user_request = request.data

            if 'search' in user_request:
                search_value = user_request['search']

                if not search_value.strip() == "":
                    satellites = Satellite.objects.all();
                    serializer = SatelliteSerializer(satellites, many=True);

                    search_value = search_value.strip()

                    data = json.loads(json.dumps(serializer.data))
                    filtered_satellites = [x for x in data if x['name'].find(search_value) != -1]

                    if len(filtered_satellites) != 0: 
                        return Response(data=filtered_satellites, status=200)
                    else:
                        return Response(data={"message": "no satellite was found"}, status=200)
                else:
                    return Response(data={"message": "search query must have a value"}, status=200)
            else:
                return Response(data={"message": "body must contain search key"}, status=400)
        else:
            return Response(data={'message':'incorrect query'}, status=400)
        
    except Satellite.DoesNotExist:
        return Response(data={'message':'There are no satellites data in the database'}, status=404)


@api_view(['GET'])
def satelliteDetail(request):
    try: 
        user_request = request.data

        if 'name' in user_request:
            name = user_request['name']
            satellite = Satellite.objects.get(name=name);
            serializer = SatelliteSerializer(satellite, many=False);
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "url must contain correct query"}, status = 400)
    except Satellite.DoesNotExist:
        return Response(data={'message':'Could not find satellite'}, status=404)
    
    

@api_view(['POST'])
def satelliteCreate(request):
    parsed_data = parseTLE(request.data)
    serializer = SatelliteSerializer(data=parsed_data);
    if serializer.is_valid():
        serializer.save()
        return Response(parsed_data)
    return Response({"message": "Unable to insert data into database", "error": serializer.errors}, status=400)

@api_view(['PUT'])
def satelliteUpdate(request):
    allowed = ["name", "tle_1", "tle_2", "description"] #data the user is allowed to change
    allow_to_change = True
    for value in allowed:
        if value not in request.data:
             allow_to_change = False
    
    if  allow_to_change :
        user_request = request.data
        if 'name' in user_request:
            name = user_request['name']
            parsed_data = parseTLE(request.data)
            satellite = Satellite.objects.get(name=name);
            serializer = SatelliteSerializer(instance=satellite, data=parsed_data);

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response({"message": "Unable to update satellite", "errors": serializer.errors}, status=405)
        else:
            return Response({"message": "url must contain correct query"}, status = 400)
    return Response({"message": "Unable to update satellite", "error": "data must contains the keys name, tle_1, tle_2, description"}, 400)

@api_view(['DELETE'])
def satelliteDelete(request):
    try: 
        user_request = request.data
        if 'name' in user_request:
            name = user_request['name']
            satellite = Satellite.objects.get(name=name);
            satellite.delete();
        else:
            return Response({"message": "url must contain correct query"}, status = 400)
    except Satellite.DoesNotExist:
        return Response(data={'message': 'item was not found'}, status=404)
    return Response(data={'message': 'item has been deleted'}, status=200)



   

