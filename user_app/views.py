from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from sensor_app.models import UserLogs

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