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
    if 'name' in user_request:
        search_value = user_request['name'].strip()

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
   



