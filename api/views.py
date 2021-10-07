from satellite.models import Satellite
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SatelliteSerializer
from satellite.models import Satellite
import logging


logger = logging.getLogger("mylogger")
#logger.info() print to command line

#
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
def satelliteDetail(_, primaryKey):
    try: 
        satellite = Satellite.objects.get(name=primaryKey);
        serializer = SatelliteSerializer(satellite, many=False);
        return Response(serializer.data, status=200)
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
def satelliteUpdate(request, primaryKey):
    allowed = ["name", "tle_1", "tle_2", "description"] #data the user is allowed to change
    change = True
    for value in allowed:
        if value not in request.data:
            change = False
    
    if change:
        parsed_data = parseTLE(request.data)
        satellite = Satellite.objects.get(name=primaryKey);
        serializer = SatelliteSerializer(instance=satellite, data=parsed_data);

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response({"message": "Unable to update satellite", "errors": serializer.errors}, status=405)
    return Response({"message": "Unable to update satellite", "error": "data must contains the keys name, tle_1, tle_2, description"}, 400)

@api_view(['DELETE'])
def satelliteDelete(_, primaryKey):
    try: 
        satellite = Satellite.objects.get(name=primaryKey);
        satellite.delete();
    except Satellite.DoesNotExist:
        return Response(data={'message': 'item was not found'}, status=404)
    return Response(data={'message': 'item has been deleted'}, status=200)



   

