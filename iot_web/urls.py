from django.contrib import admin
from django.urls import path, include
# from sensor_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sensor_app.urls")),
    path("accounts/", include("user_app.urls")),
    # path("liveSensorData/", views.LiveSensorAPIView.as_view()),
]
