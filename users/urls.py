from django.urls import path, include

from rest_framework import routers
from users import models
from users import views
# from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter()
router.register(r'userRoles', views.UserRoleViewSet)
router.register(r'User', views.UserViewSet)
router.register(r'UserProfile', views.UserProfileViewSet)
router.register(r'userPermission', views.UserPermissionViewSet)
# router.register('auth', views.AuthViewSet, basename='auth')
# router.register(r'auth', views.AuthViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/login/', views.login_user, name='login'),
    # path('api-auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('login/', views.AuthObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/logout/', views.User_logout),
    # path('api-auth/logout/', views.Logout.as_view()),
    path('api-auth/', include("rest_framework.urls")),

]