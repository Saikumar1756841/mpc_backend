from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


import datetime

from .models import Sensor, Location, LiveSensor, User, UserLogs, UserInteraction
from .serializers import (
    SensorSerializer,
    LiveSensorSerializer,
    LocationSerializer,
    UserLogsSerializer,
    UserInteractionSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def sensor_create_api(request):
    data = request.data

    # Accepting 'location' key for location ID from frontend
    location_id = data.get('location')
    if not location_id:
        return Response({"error": "Missing location ID"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        location_obj = Location.objects.get(locId=location_id)
    except Location.DoesNotExist:
        return Response({"error": "Invalid location ID"}, status=status.HTTP_400_BAD_REQUEST)

    sensor_data = {
        'name': data.get('name'),
        'sensor_id': data.get('sensor_id'),
        'unit': data.get('unit'),
        'location': location_obj.id,
    }

    serializer = SensorSerializer(data=sensor_data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Sensor created successfully!"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSensorAPIView(APIView):
    serializer_class = SensorSerializer

    def post(self, request, format=None):
        sensor_id = request.data.get("sensor_id")
        if not sensor_id:
            return Response({"error": "Missing sensor_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
            serializer = self.serializer_class(sensor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Sensor.DoesNotExist:
            return Response({"error": "No sensor found with these credentials"}, status=status.HTTP_404_NOT_FOUND)


class LiveSensorAPIView(APIView):
    serializer_class = LiveSensorSerializer

    def get(self, request):
        return Response({"success": "Get the data"}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        res = request.data

        sensor_id = res.get('id')
        data = res.get('data')

        if sensor_id is None or data is None:
            return Response({"error": "Missing 'id' or 'data' in request"}, status=status.HTTP_400_BAD_REQUEST)

        timestamp = datetime.datetime.now()

        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
        except Sensor.DoesNotExist:
            return Response({"error": "No sensor found with this given ID"}, status=status.HTTP_404_NOT_FOUND)

        livedata = LiveSensor(sensor=sensor, data=data, timestamp=timestamp)
        livedata.save()

        return Response({"success": "Data received and saved"}, status=status.HTTP_201_CREATED)


class SensorAPIView(APIView):
    serializer_class = SensorSerializer

    def get(self, request, format=None):
        all_sensors = Sensor.objects.all()
        serializer = self.serializer_class(all_sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        sensor_id = request.data.get("sensor_id")
        if not sensor_id:
            return Response({"error": "Missing sensor_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
            sensor.delete()
            return Response({"message": "Sensor deleted successfully"}, status=status.HTTP_200_OK)
        except Sensor.DoesNotExist:
            return Response({"error": "No sensor found with this ID"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        data = request.data
        name = data.get('name')
        sensor_id = data.get('sensor_id')
        unit = data.get('unit')
        location_id = data.get('locationID')

        if not all([name, sensor_id, unit, location_id]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = Location.objects.get(locId=location_id)
        except Location.DoesNotExist:
            return Response({"error": "No location found with this ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Update existing sensor
        sensor_qs = Sensor.objects.filter(sensor_id=sensor_id)
        if sensor_qs.exists():
            sensor = sensor_qs.first()
            sensor.name = name
            sensor.unit = unit
            sensor.location = location
            sensor.save()
            return Response({"message": "Sensor updated successfully"}, status=status.HTTP_200_OK)

        # Create new sensor
        sensor = Sensor(name=name, sensor_id=sensor_id, unit=unit, location=location)
        sensor.save()
        return Response({"message": "Sensor added successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        data = request.data
        sensor_id = data.get('sensor_id')
        if not sensor_id:
            return Response({"error": "Missing sensor_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(sensor_id=sensor_id)
        except Sensor.DoesNotExist:
            return Response({"error": "Sensor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(sensor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationAPIView(APIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        if user.is_staff:
            locations = Location.objects.all()
        else:
            locations = Location.objects.filter(user=user)
        serializer = self.serializer_class(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        location_id = request.data.get("location_id")
        if not location_id:
            return Response({"error": "Missing location_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = Location.objects.get(locId=location_id)
            location.delete()
            return Response({"message": "Location deleted successfully"}, status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({"error": "No location found with this ID"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, format=None):
        data = request.data
        location_id = data.get('locId')
        if not location_id:
            return Response({"error": "Missing locId"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            location = Location.objects.get(locId=location_id)
        except Location.DoesNotExist:
            return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(location, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceAPIView(APIView):
    def get(self, request):
        devices = Location.objects.all()
        serializer = LocationSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user_id = request.data.get("user")
        device_name = request.data.get("name")

        if not all([user_id, device_name]):
            return Response({"error": "Missing user or name"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        device = Location(user=user, name=device_name)
        device.save()
        return Response({"message": "Device added successfully"}, status=status.HTTP_201_CREATED)


class UserLogsAPIView(APIView):
    def get(self, request):
        all_userlogs = UserLogs.objects.order_by('-timestamp')
        serializer = UserLogsSerializer(all_userlogs, many=True)

        # Mark all logs as seen
        for log in all_userlogs:
            if not log.isSeen:
                log.isSeen = True
                log.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        data = request.data.get('data')
        if not data:
            return Response({"error": "Missing log data"}, status=status.HTTP_400_BAD_REQUEST)

        log = UserLogs(userName=user.name, data=data)
        log.save()
        return Response({"message": "Logs saved successfully"}, status=status.HTTP_201_CREATED)


class UserInteractionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = datetime.date.today()

        # Check if an entry exists for this user and today's date
        obj, created = UserInteraction.objects.get_or_create(user=user, date=today, defaults={'time': '0'})

        # Increase time by 5 (assume time stored as string integer)
        try:
            current_time = int(obj.time)
        except (ValueError, TypeError):
            current_time = 0

        current_time += 5
        obj.time = str(current_time)
        obj.save()

        return Response({"message": "User interaction time updated"}, status=status.HTTP_200_OK)

    def get(self, request):
        user_interactions = UserInteraction.objects.filter(user=request.user)
        serializer = UserInteractionSerializer(user_interactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
