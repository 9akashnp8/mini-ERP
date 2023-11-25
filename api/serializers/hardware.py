from rest_framework import serializers

from employee.models import Location
from .employee import LocationSerializer
from hardware.models import Laptop, LaptopBrand, Building


class LaptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = "__all__"
        depth = 1


class LaptopCreateSerializer(LaptopSerializer):
    class Meta(LaptopSerializer.Meta):
        depth = 0


class LaptopBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaptopBrand
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
