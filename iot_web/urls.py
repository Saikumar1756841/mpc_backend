from django.contrib import admin
from django.urls import path, include
# from sensor_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("sensor_app.urls")),
    path("accounts/", include("user_app.urls")),
    # path("liveSensorData/", views.LiveSensorAPIView.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('user_app.urls')),
]
