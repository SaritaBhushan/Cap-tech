from django.shortcuts import render
from users.serializers import UserRoleSerializer,  UserPermissionSerializer, UserSerializer, UserProfileSerializer # UserDetailsSerializer,
from users.models import User_role,  User_permission, UserProfile, User_login_status # User_details,
from users.serializers import UserLoginSerializer
from users.serializers import AuthTokenObtainPairSerializer

# from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.contrib.auth import logout
from datetime import datetime

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# from django.contrib.auth import get_user_model
# from django.core.exceptions import ImproperlyConfigured

from . import serializers
from .utils import get_and_authenticate_user
from django.contrib.auth.models import User

class LoginAPIView(APIView):
    print("@@@1 User_login 1@@")
    def post(self, request):
        print("@@@2 User_login 2@@")

class Logout(APIView):
    print("@@@1 User_logout @")

    def get(self, request, format=None):
        print("@@@1User_logout")
        # simply delete the token to force a login
        try:
            request.user.auth_token.delete()
        except Exception as e:
            pass
        # logout(request)

        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def login_user(request):
    print("@request.user: ", request.user, request.user.id)
    try:
        obj=User_login_status.objects.get(user=request.user)
        print(obj)
        obj.status = True
        obj.login = datetime.now()
        # obj.logout = datetime.now()
        
    except Exception as e:
        obj= User_login_status(user=request.user, status=True, login=datetime.now(), logout= datetime.now())
    finally:
        obj.save()

    return Response( status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):
    # print("@@@User_logout: Done",  request, request.method, request.user, request.data)
    print("@request.user: ", request.user, request.user.id)
    try:
        obj=User_login_status.objects.get(user=request.user)
        print(obj)
        obj.status = False
        obj.logout = datetime.now()
        # obj.save()
    except Exception as e:
        obj= User_login_status(user=request.user, status=False, login=datetime.now(), logout= datetime.now())
    finally:
        obj.save()
    
    try:
        request.user.auth_token.delete()
    except Exception as e:
        pass
    
    logout(request)
    return Response('User Logged out successfully')


class AuthObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AuthTokenObtainPairSerializer


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User_role.objects.all()
    serializer_class = UserRoleSerializer
    # authentication_classes=[JWTAuthentication, SessionAuthentication, BasicAuthentication]
    # permission_classes=[IsAuthenticated]

class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User_permission.objects.all()
    serializer_class = UserPermissionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # authentication_classes=[JWTAuthentication, SessionAuthentication, BasicAuthentication]
    # permission_classes=[IsAuthenticated]