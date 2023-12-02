from rest_framework import serializers

from hardware.models import (
    Laptop,
    LaptopV2,
    LaptopBrand,
    Hardware,
    HardwareType,
    HardwareOwner,
    HardwareCondition,
)


class HardwareListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        exclude = ["id"]
        depth = 1


class HardwareCreateUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hardware
        exclude = ["id"]
        extra_kwargs = {
            "type": {"required": True},
            "owner": {"required": True},
            "condition": {"required": True},
            "location": {"required": True},
            "building": {"required": True},
        }


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


class LaptopV1ListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = "__all__"
        depth = 1


class LaptopV1CreateSerializer(LaptopV1ListRetrieveSerializer):
    class Meta(LaptopV1ListRetrieveSerializer.Meta):
        depth = 0


class LaptopV2CreateSerializer(serializers.ModelSerializer):
    hardware_id = HardwareCreateUpdateDestroySerializer()

    class Meta:
        model = LaptopV2
        exclude = ["id"]
        extra_kwargs = {"brand": {"required": True}, "screen_size": {"required": True}}

    def create(self, validated_data):
        hardware_data = validated_data.pop("hardware_id")
        return LaptopV2.objects.create(hardware_data, validated_data)


class LaptopV2ListRetrieveSerializer(serializers.ModelSerializer):
    hardware_id = HardwareListRetrieveSerializer(read_only=True)

    class Meta:
        model = LaptopV2
        exclude = ["id"]
        depth = 1


class LaptopBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaptopBrand
        fields = "__all__"
