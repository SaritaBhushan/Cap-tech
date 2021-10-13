from django.contrib import admin

# Register your models here.
from users.models import User_role,  User_permission, UserProfile, User_login_status 

# Register your models here.
admin.site.register(User_role)
admin.site.register(User_permission)
admin.site.register(UserProfile)
# admin.site.register(User_login_status)