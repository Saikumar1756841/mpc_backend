from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from sensor_app.models import Sensor

from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from sensor_app.models import UserLogs
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class DeviceCreateView(APIView):
    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_user_with_sensors(request):
    try:
        data = request.data
 
        email = data.get('email')
        username = data.get('name')  # from your form's "Name"
        password = data.get('password')
        confirm_password = data.get('confirm_password') or data.get('confirmPassword')
        is_admin = data.get('is_admin', False)
        sensor_ids = data.get('sensor_ids', []) or data.get('sensors') or []

        # Validate required fields
        if not email or not username or not password or not confirm_password:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create user
            user = User.objects.create_user(
                name=username,
                email=email,
                password=password,
                tc=True,   # or get from request if needed
                is_admin=is_admin  # Mark admin user if checked
            )

            # Assign sensors to user (assuming ForeignKey in Sensor model)
            sensors = Sensor.objects.filter(id__in=sensor_ids)
            for sensor in sensors:
                sensor.user = user
                sensor.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# API to get the user information using authentication token
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        print(user.name)
        serialized_users = UserProfileSerializer(user).data
        return Response(serialized_users, status=status.HTTP_200_OK)

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)

    print(request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    # Creating Log
    if user.is_staff is False:
      log = UserLogs(userName=user.name, data="Created Account")
      log.save()
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')

    print(email, "-", password)

    # return Response({'token':"get data", 'msg':'Login Success'}, status=status.HTTP_200_OK)

    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)

      # Creating Log
      if user.is_staff is False:
        log = UserLogs(userName=user.name, data="Logged in")
        log.save()

      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
# Route to get all the users
class GetAllUsersAPIView(APIView):
    def get(self, request, format=None):
        all_users = User.objects.all()
        user_serialized = UserProfileSerializer(all_users, many=True).data
        return Response(user_serialized, status=status.HTTP_200_OK)

# class UserLogoutAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     # authentication_classes = [TokenAuthentication]
#     def get(self, request):
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)