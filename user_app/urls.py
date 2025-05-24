from django.urls import path
from .views import UserLoginView, UserRegistrationView, UserProfileAPIView, GetAllUsersAPIView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('getUser/', UserProfileAPIView.as_view(), name='getUser'),
    path('getAllUsers/', GetAllUsersAPIView.as_view(), name='getAllUsers'),
    # path('logout/', UserLogoutAPIView.as_view(), name='logout'),
]