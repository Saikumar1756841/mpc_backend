from django.shortcuts import render
from .serializers import SensorSerializer, LiveSensorSerializer, LocationSerializer, UserLogsSerializer, UserInteractionSerializer
from .models import Sensor, Location, LiveSensor, User, UserLogs, UserInteraction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import ast
import random
import requests
from decouple import config
import datetime
from rest_framework.permissions import IsAuthenticated


class GetSensorAPIView(APIView):
    sensor_serializer_class = SensorSerializer
    # Get a particular sensor

    def post(self, request, format=None):
        data = request.data
        sensor_id = data["sensor_id"]
        if (Sensor.objects.filter(sensor_id=sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id=sensor_id).first()
            return Response(req_sensor, status=status.HTTP_200_OK)
        return Response({"Error": "No Sensor found with these credentials"}, status=status.HTTP_400_BAD_REQUEST)

# In this class, we receive data of sensors coming from Microcontrollers.


class LiveSensorAPIView(APIView):
    live_sensor_serializer_class = LiveSensorSerializer

    def get(self, request):
        return Response({"Success": "Get the data"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        res = request.data
        # print(res)
        data = res['data']
        sensor_id = res['id']
        timestamp = str(datetime.datetime.now())
        print(res)
        # return Response({"Success": "Get the data"}, status=status.HTTP_200_OK)

        # Finding sensor with the given id
        if (Sensor.objects.filter(sensor_id=sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id=sensor_id).first()
            livedata = LiveSensor(
                sensor=req_sensor, data=data, timestamp=timestamp)
            livedata.save()
            return Response({"Success": "Get the data"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "No sensor found with this given ID"}, status=status.HTTP_404_NOT_FOUND)


class SensorAPIView(APIView):
    sensor_serializer_class = SensorSerializer

    # Get all sensors
    def get(self, request, format=None):
        all_sensors = Sensor.objects.all()
        stu_serialized = SensorSerializer(all_sensors, many=True)
        json_object = JSONRenderer().render(stu_serialized.data)
        return HttpResponse(json_object, content_type="application/Json")

    # Delete the sensor
    def delete(self, request, format=None):
        data = request.data
        sensor_id = data["sensor_id"]
        if (Sensor.objects.filter(sensor_id=sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id=sensor_id).first()
            req_sensor.delete()
            location = Location.objects.all()
            loc_serialized = LocationSerializer(location, many=True)
            return Response(loc_serialized.data, status=status.HTTP_200_OK)
        return Response("No Sensor found with this ID", status=status.HTTP_400_BAD_REQUEST)

    # API to add/update a new sensor
    def post(self, request, format=None):
        data = request.data
        name = data['name']
        id = data['sensor_id']
        unit = data['unit']
        locationID = data['locationID']

        # Checking the exixting of a sensor
        if Sensor.objects.filter(sensor_id=id).exists():
            if (Location.objects.filter(locId=locationID).exists()):
                location = Location.objects.filter(locId=locationID).first()
                sensor = Sensor.objects.filter(sensor_id=id).first()
                sensor.location = location
                sensor.name = name
                sensor.unit = unit
                sensor.save()
                return Response("Data Updated Succesfully", status=status.HTTP_200_OK)
            else:
                return Response("No Location found with this ID", status=status.HTTP_400_BAD_REQUEST)
        else:
            # Check locationID is correct or not
            if (Location.objects.filter(locId=locationID).exists()):
                location = Location.objects.filter(locId=locationID).first()
                sensor = Sensor(location=location, name=name,
                                sensor_id=id, unit=unit)
                sensor.save()
                return Response("Sensor added succesfully", status=status.HTTP_200_OK)
            else:
                print("No Location found with this ID")
                return Response("No Location found with this ID", status=status.HTTP_400_BAD_REQUEST)

    # API to update the sensor data

    def put(self, request, format=None):
        data = request.data
        sensor_serializer = self.sensor_serializer_class(data=data)
        if sensor_serializer.is_valid():
            sensor_serializer.save()
            return Response(sensor_serializer, status=status.HTTP_200_OK)
        else:
            return Response(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationAPIView(APIView):
    location_serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    # Get all locations

    def get(self, request, format=None):
        user = request.user
        all_locations = []
        if user.is_staff is True:
            all_locations = Location.objects.all()
        else:
            all_locations = Location.objects.filter(user=user)
        loc_serialized = LocationSerializer(all_locations, many=True).data
        return Response(loc_serialized, status=status.HTTP_200_OK)

    # Delete the location
    def delete(self, request, format=None):
        data = request.data
        sensor_id = data["sensor_id"]
        if (Sensor.objects.filter(sensor_id=sensor_id).exists()):
            req_sensor = Sensor.objects.filter(sensor_id=sensor_id).first()
            req_sensor.delete()
            all_sensors = Sensor.objects.all()
            stu_serialized = SensorSerializer(all_sensors, many=True)
            return Response(stu_serialized.data, status=status.HTTP_200_OK)
        return Response({"Error": "No Sensor found with this ID"}, status=status.HTTP_400_BAD_REQUEST)

    # API to update the location data
    def put(self, request, format=None):
        data = request.data
        sensor_serializer = self.sensor_serializer_class(data=data)
        if sensor_serializer.is_valid():
            sensor_serializer.save()
            return Response(sensor_serializer, status=status.HTTP_200_OK)
        else:
            return Response(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceAPIView(APIView):
    # API to get all devices
    def get(self, request):
        all_devices = Location.objects.all()
        devices_serialized = LocationSerializer(all_devices, many=True).data
        return Response(devices_serialized, status=status.HTTP_200_OK)

    # API to add a new device

    def post(self, request, format=None):
        data = request.data
        userId = data["user"]
        deviceName = data["name"]
        user = User.objects.filter(id=userId).first()
        device = Location(user=user, name=deviceName)
        device.save()
        return Response({"Success"}, status=status.HTTP_200_OK)


class UserLogsAPIView(APIView):
    # Get all user logs
    def get(self, request):
        all_userlogs = UserLogs.objects.order_by('-timestamp')
        userlogs_serialized = UserLogsSerializer(all_userlogs, many=True).data
        # Marking all previously sent logs
        for log in all_userlogs:
            log.isSeen = True
            log.save()
        return Response(userlogs_serialized, status=status.HTTP_200_OK)

    # Post the logs
    def post(self, request):
        user = request.user
        data = request.data
        log = UserLogs(userName=user.name, data=data['data'])
        log.save()
        return Response({"Success": "Logs saved succesfully"}, status=status.HTTP_200_OK)
    

class UserInteractionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        print(user.name)
        if UserInteraction.objects.filter(date=datetime.date.today()).exists():
            obj = UserInteraction.objects.filter(date=datetime.date.today()).first()
            time = obj.time
            time = int(time) + 5
            obj.time = str(time)
            obj.save()
        else:
            obj = UserInteraction(user=user, time="0")
            obj.save()
        return Response({"Success": "Get the data"}, status=status.HTTP_200_OK)

        all_userlogs = UserLogs.objects.order_by('-timestamp')
        userlogs_serialized = UserLogsSerializer(all_userlogs, many=True).data
        # Marking all previously sent logs
        for log in all_userlogs:
            log.isSeen = True
            log.save()
        return Response(userlogs_serialized, status=status.HTTP_200_OK)
    
    def get(self, request):
        user_interaction = UserInteraction.objects.filter(user=request.user).all()
        user_interaction_serialized = UserInteractionSerializer(user_interaction, many=True).data
        return Response(user_interaction_serialized, status=status.HTTP_200_OK)

