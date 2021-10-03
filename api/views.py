from satellite.models import Satellite
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SatelliteSerializer
from satellite.models import Satellite
from tletools import TLE

# Create your views here.
@api_view(['GET'])
def apiOverview(response):
    data = {
        'message': 'This is the satellite api route',
        'routes': {
            "/api/satellites/": {
                'request-type': 'GET',
                'description': "returns all satellites in the database",
            },
            "/api/satellite/:id/": {
                'request-type': 'GET',
                'description': "returns a satellite in the database given its id",
            },
            "/api/satellite-create/": {
                'request-type': 'POST',
                'description': "adds a new satellite entry into the database",
            },
             "/api/satellite-update/:id/": {
                'request-type': 'PUT',
                'description': "updates a satellite given its id",
            },
             "/api/satellite-delete/:id/": {
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
        satellite_list = [];
        for satellite in serializer.data:
            tle_data = TLE.from_lines(satellite["name"], satellite["tle_1"], satellite["tle_2"])
            dict_tle_data = tle_data.asdict()
            dict_tle_data["description"] = satellite["description"]
            dict_tle_data["id"] = satellite["id"]
            dict_tle_data["tle_1"] = satellite["tle_1"]
            dict_tle_data["tle_2"] = satellite["tle_2"]
            satellite_list.append(dict_tle_data)
        return Response(satellite_list, status=200)
    except Satellite.DoesNotExist:
        return Response(data={'message':'There is no satellite data in the database'}, status=404)

@api_view(['GET'])
def satelliteDetail(request, primaryKey):
    try: 
        satellite = Satellite.objects.get(id=primaryKey);
        serializer = SatelliteSerializer(satellite, many=False);
        tle_data = TLE.from_lines(serializer.data["name"], serializer.data["tle_1"], serializer.data["tle_2"])
        dict_tle_data = tle_data.asdict()
        dict_tle_data["description"] = serializer.data["description"]
        dict_tle_data["id"] = serializer.data["id"]
        dict_tle_data["tle_1"] = serializer.data["tle_1"]
        dict_tle_data["tle_2"] = serializer.data["tle_2"]
        return Response(dict_tle_data, status=200)
    except Satellite.DoesNotExist:
        return Response(data={'message':'Could not find satellite'}, status=404)

@api_view(['POST'])
def satelliteCreate(request):
    serializer = SatelliteSerializer(data=request.data);
    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data)
    return Response({"message": "Unable to insert data into database"}, status=400)

@api_view(['PUT'])
def satelliteUpdate(request, primaryKey):
    satellite = Satellite.objects.get(id=primaryKey);
    serializer = SatelliteSerializer(instance=satellite, data=request.data);

    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data, status=200)
    return Response({"message": "Unable to update satellite"}, status=405)

@api_view(['DELETE'])
def satelliteDelete(request, primaryKey):
    try: 
        satellite = Satellite.objects.get(id=primaryKey);
        satellite.delete();
    except Satellite.DoesNotExist:
        return Response(data={'message': 'item was not found'}, status=404)
    return Response(data={'message': 'item has been deleted'}, status=200)

       

