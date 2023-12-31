from rest_framework import serializers
from django.contrib.auth.models import User

from common.models import HardwareAppSetting, EmployeeAppSetting
from hardware.models import Building
from employee.models import Location
from .employee import LocationSerializer


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


class BuildingSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Building
        fields = "__all__"


class BuildingRetrieveListDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"
        depth = 1


class BuildingCreateUpdateSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    class Meta:
        model = Building
        fields = "__all__"
