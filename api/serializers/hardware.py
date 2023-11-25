from rest_framework import serializers

from hardware.models import Laptop, LaptopBrand, HardwareType


class HardwareTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareType
        fields = "__all__"


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
