from rest_framework import serializers
from .models import Sensor, LiveSensor, Location, UserLogs, UserInteraction
from django.contrib.auth.models import User


class CreateUserWithSensorsSerializer(serializers.ModelSerializer):
    sensors = serializers.PrimaryKeyRelatedField(
        queryset=Sensor.objects.all(),
        many=True,
        write_only=True
    )
    confirmPassword = serializers.CharField(write_only=True)
    is_admin = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirmPassword', 'sensors', 'is_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        sensors = validated_data.pop('sensors')
        validated_data.pop('confirmPassword')
        is_admin = validated_data.pop('is_admin', False)

        user = User.objects.create_user(**validated_data)
        if is_admin:
            user.is_staff = True
            user.is_superuser = True
        user.save()

        # TODO: Assign sensors to user if you have a relation
        # Example:
        # for sensor in sensors:
        #     UserSensorAssignment.objects.create(user=user, sensor=sensor)

        return user


class UserInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'


class LiveSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveSensor
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    live_sensors = LiveSensorSerializer(many=True, read_only=True)
    location = serializers.SlugRelatedField(
        slug_field='locId',
        queryset=Location.objects.all()
    )

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'sensor_id', 'unit', 'location', 'live_sensors']
        read_only_fields = ['id', 'live_sensors']


class LocationSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}


class UserLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogs
        fields = '__all__'
