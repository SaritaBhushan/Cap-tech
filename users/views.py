from django.shortcuts import render
from users.serializers import UserRoleSerializer,  UserPermissionSerializer, UserSerializer, UserProfileSerializer # UserDetailsSerializer,
from users.models import User_role,  User_permission, UserProfile, User_login_status # User_details,
from users.serializers import EmptySerializer, UserLoginSerializer

# from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ImproperlyConfigured

from . import serializers
# from .utils import get_and_authenticate_user
from django.contrib.auth.models import User


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = User_role.objects.all()
    serializer_class = UserRoleSerializer

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

    # authentication_classes=[JWTAuthentication, SessionAuthentication, BasicAuthentication]
    # permission_classes=[IsAuthenticated]

    # serializer_class = EmptySerializer
    # serializer_classes = {
    #     'login': UserLoginSerializer,
    #      'register': UserSerializer,
    #      'logout': EmptySerializer,
    #  }

    # @action(methods=['POST', ], detail=False)
    # def login(self, request):
    #     print("@@@@@@@@@@@@@data=",request.data)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = get_and_authenticate_user(**serializer.validated_data)
    #     data = serializers.AuthUserSerializer(user).data

    #     userlogstatusObj = User_login_status.objects.filter(user__id=data["id"])
    #     if userlogstatusObj.exists():
    #         userlogstatusObj = userlogstatusObj.first()
    #         print(" update")
    #     else:
    #         userlogstatusObj = User_login_status()
    #         print(" New")
    #     userlogstatusObj.status = True
    #     userlogstatusObj.save()
    
    
    #     return Response(data=data, status=status.HTTP_200_OK)

    # @action(methods=['POST', ], detail=False)
    # def logout(self, request):
        
    #     userlogstatusObj = User_login_status.objects.filter(user__id=request.data["id"])
    #     if userlogstatusObj.exists():
    #         userlogstatusObj = userlogstatusObj.first()
    #         print(" update")
    #     else:
    #         userlogstatusObj = User_login_status()
        
    #     userlogstatusObj.status = False
    #     userlogstatusObj.save()

    #     logout(request)
    #     data = {'success': 'Sucessfully logged out'}


    #     return Response(data=data, status=status.HTTP_200_OK)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # authentication_classes=[JWTAuthentication, SessionAuthentication, BasicAuthentication]
    # permission_classes=[IsAuthenticated]