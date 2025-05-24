from django.urls import path, include
from .views import SensorAPIView, LocationAPIView, LiveSensorAPIView, DeviceAPIView, UserLogsAPIView, UserInteractionAPIView

urlpatterns = [
    path('sensorDataAPI/', SensorAPIView.as_view()),
    path('locationDataAPI/', LocationAPIView.as_view()),
    path('liveSensorData/', LiveSensorAPIView.as_view()),
    path('device/', DeviceAPIView.as_view()),
    path('getUserLogs/', UserLogsAPIView.as_view()),
    path('getUserInteraction/', UserInteractionAPIView.as_view()),
]