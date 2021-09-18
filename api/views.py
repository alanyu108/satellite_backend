from satellite.models import Satellite
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SatelliteSerializer
from satellite.models import Satellite

# Create your views here.
@api_view(['GET'])
def apiOverview(response):
    return Response(data={'message': 'This is the satellite api route'})

@api_view(['GET'])
def satelliteList(request):
    try: 
        satellites = Satellite.objects.all();
        serializer = SatelliteSerializer(satellites, many=True);
        return Response(serializer.data, status=200)
    except Satellite.DoesNotExist:
        return Response(data={'message':'There is no satellite data in the database'}, status=404)

@api_view(['GET'])
def satelliteDetail(request, primaryKey):
    try: 
        satellite = Satellite.objects.get(id=primaryKey);
        serializer = SatelliteSerializer(satellite, many=False);
        return Response(serializer.data)
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

       

