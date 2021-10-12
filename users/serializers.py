from rest_framework import serializers, fields
from users.models import User_role,  User_permission, UserProfile #User_details,
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# User = get_user_model()


import hashlib
import base64
from django.utils.crypto import (
    get_random_string, pbkdf2,
)

# import random

#SET VALUES
algorithm = "pbkdf2_sha256"
iterations = 36000
length=12
allowed_chars='abcdefghijklmnopqrstuvwxyz''ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_role
        fields = '__all__'

class  UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        min_length=6,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
        )
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # create user
        print(validated_data["password"])

        # Salt
        import random
        random = random.SystemRandom()
        salt =''.join(random.choice(allowed_chars) for i in range(length))

        # Hash
        digest = hashlib.sha256
        hash = pbkdf2(validated_data["password"], salt, iterations, digest=digest)
        hash = base64.b64encode(hash).decode('ascii').strip()

        # encoded_password
        encoded_password="%s$%d$%s$%s" % (algorithm, iterations, salt, hash)
        
        print("@encoded_password:", encoded_password)

        user = User.objects.create(
            username = validated_data["username"],
            password =  encoded_password, # validated_data["password"],
            # name  = validated_data["name"],
            # surname  = validated_data["surname"],
            email  = validated_data["email"],
            # dob = validated_data["dob"],
            # role  = validated_data["role"],

            # Activation Status
            # status = validated_data["status"],
            # Time Stamp information
            # created = validated_data["created"],
            # updated  = validated_data["updated"],
            )
        return user

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserPermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_permission
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


# class AuthUserSerializer(serializers.ModelSerializer):
#     auth_token = serializers.SerializerMethodField()

#     class Meta:
#          model = User
#          fields = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
#          read_only_fields = ('id', 'is_active', 'is_staff')
    
#     def get_auth_token(self, obj):
#         token = Token.objects.create(user=obj)
#         return token.key

class EmptySerializer(serializers.Serializer):
    pass

# class UserRegisterSerializer(serializers.ModelSerializer):
#     """
#     A user serializer for registering the user
#     """

#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password', 'first_name', 'last_name')

#     def validate_email(self, value):
#         user = User.objects.filter(email=email)
#         if user:
#             raise serializers.ValidationError("Email is already taken")
#         return BaseUserManager.normalize_email(value)

#     def validate_password(self, value):
#         password_validation.validate_password(value)
#         return value