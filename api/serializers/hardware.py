from rest_framework import serializers

from hardware.models import (
    Laptop,
    LaptopBrand,
    HardwareType,
    HardwareOwner,
    HardwareCondition,
)


class HardwareTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareType
        fields = "__all__"


class HardwareOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareOwner
        fields = "__all__"


class HardwareConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareCondition
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
