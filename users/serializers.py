from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User , Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","company","role"]