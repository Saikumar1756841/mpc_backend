from django.urls import path, include
from .views import sensor_create_api
from .views import SensorAPIView, LocationAPIView, LiveSensorAPIView, DeviceAPIView, UserLogsAPIView, UserInteractionAPIView

urlpatterns = [
    path('sensorDataAPI/', SensorAPIView.as_view()),
    path('locationDataAPI/', LocationAPIView.as_view()),
    path('liveSensorData/', LiveSensorAPIView.as_view()),
    path('device/', DeviceAPIView.as_view()),
    path('getUserLogs/', UserLogsAPIView.as_view()),
    path('api/sensorDataAPI/', sensor_create_api, name='sensor-create-api'),
    path('getUserInteraction/', UserInteractionAPIView.as_view()),
]