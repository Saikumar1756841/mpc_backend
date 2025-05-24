from rest_framework import serializers
from .models import Sensor, LiveSensor, Location, UserLogs, UserInteraction
from django.contrib.auth.models import User

class UserInteractionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserInteraction
        fields = ('__all__')

class LiveSensorSerializer(serializers.ModelSerializer):    
    class Meta:
        model = LiveSensor
        fields = ('__all__')

class SensorSerializer(serializers.ModelSerializer):
    live_sensors_set = LiveSensorSerializer(source='live_sensors', many=True, read_only=True)
    class Meta:
        model = Sensor
        fields = ('__all__')

class LocationSerializer(serializers.ModelSerializer):
    sensors_set = SensorSerializer(source='sensors', many=True, read_only=True)
    class Meta:
        model = Location
        fields = ('__all__')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

class UserLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogs
        fields = ('__all__')