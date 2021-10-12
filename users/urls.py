from django.urls import path, include

from rest_framework import routers
from users import models
from users import views

router = routers.DefaultRouter()
router.register(r'userRoles', views.UserRoleViewSet)
router.register(r'User', views.UserViewSet)
router.register(r'UserProfile', views.UserProfileViewSet)
router.register(r'userPermission', views.UserPermissionViewSet)
# router.register('auth', views.AuthViewSet, basename='auth')
# router.register(r'auth', views.AuthViewSet)

urlpatterns = [
	path('', include(router.urls)),
]