from satellite.models import Satellite
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SatelliteSerializer
from satellite.models import Satellite
from api.functions import parseTLE
from urllib.parse import parse_qs

import logging
logger = logging.getLogger("mylogger")
#logger.info() print to command line

# Create your views here.
@api_view(['GET'])
def apiOverview(response):
    data = {
        'message': 'This is the satellite api route',
        'routes': {
            "satellites/": {
                'request-type': 'GET',
                'description': "returns all satellites in the database",
                'example': "/api/satellites/", 
            },
            "satellite/:name/": {
                'request-type': 'GET',
                'description': "returns a satellite in the database given its name",
                'example': "/api/satellite/name=CALSPHERE 1/", 
            },
            "satellite-create/": {
                'request-type': 'POST',
                'description': "adds a new satellite entry into the database, data sent to this route must have the keys name, tle_1, tle_2 and description",
                'example': "/api/satellite-create/", 
            },
             "satellite-update/:name/": {
                'request-type': 'PUT',
                'description': "updates a satellite given its name,  data sent to this route must have the keys name, tle_1, tle_2 and description",
                'example': "/api/satellite-update/name=CALSPHERE 1/", 
            },
             "satellite-delete/:name/": {
                'request-type': 'DELETE',
                'description': "delete a satellite given its name",
                'example': "/api/satellite-delete/name=CALSPHERE 1/",
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
def satellitePage(_, query):
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
                return Response(filtered_satellite, status=200)
            else:
                return Response(data={'message':'page number must be an integer'}, status=400)
        else:
            return Response(data={'message':'incorrect query'}, status=400)
    except Satellite.DoesNotExist:
        return Response(data={'message':'There are no satellites data in the database'}, status=404)


@api_view(['GET'])
def satelliteDetail(_, query):
    try: 
        parsed_query = parse_qs(query) 
        if 'name' in parsed_query:
            name = parsed_query['name'][0]
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
def satelliteUpdate(request, query):
    allowed = ["name", "tle_1", "tle_2", "description"] #data the user is allowed to change
    allow_to_change = True
    for value in allowed:
        if value not in request.data:
             allow_to_change     = False
    
    if  allow_to_change :
        parsed_query = parse_qs(query) 
        if 'name' in parsed_query:
            name = parsed_query['name'][0]
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
def satelliteDelete(_, query):
    try: 
        parsed_query = parse_qs(query) 
        if 'name' in parsed_query:
            name = parsed_query['name'][0]
            satellite = Satellite.objects.get(name=name);
            satellite.delete();
        else:
            return Response({"message": "url must contain correct query"}, status = 400)
    except Satellite.DoesNotExist:
        return Response(data={'message': 'item was not found'}, status=404)
    return Response(data={'message': 'item has been deleted'}, status=200)



   

