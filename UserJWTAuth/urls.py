from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/v0/', include('users.urls')),
    # # Jwt Token
    # path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]
