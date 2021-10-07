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
            },
            "satellite/:id/": {
                'request-type': 'GET',
                'description': "returns a satellite in the database given its id",
            },
            "satellite-create/": {
                'request-type': 'POST',
                'description': "adds a new satellite entry into the database",
            },
             "satellite-update/:id/": {
                'request-type': 'PUT',
                'description': "updates a satellite given its id",
            },
             "satellite-delete/:id/": {
                'request-type': 'DELETE',
                'description': "delete a satellite given its id",
            },
        }
    }
    return Response(data=data)

@api_view(['GET'])
def satelliteList(request):
    try: 
        satellites = Satellite.objects.all();
        serializer = SatelliteSerializer(satellites, many=True);
        return Response(serializer.data, status=200)
    except Satellite.DoesNotExist:
        return Response(data={'message':'There is no satellite data in the database'}, status=404)

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
            return Response({"message": "url must contain query"}, status = 400)
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
            return Response({"message": "url must contain query"}, status = 400)
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
            return Response({"message": "url must contain query"}, status = 400)
    except Satellite.DoesNotExist:
        return Response(data={'message': 'item was not found'}, status=404)
    return Response(data={'message': 'item has been deleted'}, status=200)



   

