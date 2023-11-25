from rest_framework import serializers
from django.contrib.auth.models import User

from common.models import HardwareAppSetting, EmployeeAppSetting


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email_address" "username",
        ]


class EmployeeAppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAppSetting
        fields = "__all__"


class HardwareAppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareAppSetting
        fields = "__all__"
