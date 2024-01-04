from django.core.exceptions import ValidationError
from rest_framework import serializers

from hardware.models import (
    Laptop,
    LaptopV2,
    LaptopBrand,
    Hardware,
    HardwareType,
    HardwareOwner,
    HardwareCondition,
    HardwareAssignment,
)
from employee.models import Employee


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


class HardwareAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareAssignment
        fields = "__all__"


class HardwareAssignmentDetailSerializer(serializers.ModelSerializer):
    hardware = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = HardwareAssignment
        fields = "__all__"

    def get_hardware(self, obj):
        hardware = Hardware.objects.select_related("type").get(id=obj.hardware.id)
        return {
            "uuid": hardware.uuid,
            "hardware_id": hardware.hardware_id,
            "serial_no": hardware.serial_no,
            "type": {"id": hardware.type.id, "name": hardware.type.name},
        }

    def get_employee(self, obj):
        employee = Employee.objects.get(emp_id=obj.employee.emp_id)
        return {"emp_id": employee.emp_id, "lk_emp_id": employee.lk_emp_id}


class HardwareAssignmentCreateSerializer(serializers.ModelSerializer):
    hardware = serializers.UUIDField()

    class Meta:
        model = HardwareAssignment
        fields = ["hardware", "employee", "assignment_date"]
        extra_kwargs = {
            "hardware": {"required": True},
            "employee": {"required": True},
            "assignment_date": {"required": True},
        }

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
        except ValidationError:
            raise serializers.ValidationError(
                "Hardware Already Assigned to Employee, Please Return Existing Hardware"
            )
        else:
            return instance

    def validate_hardware(self, value):
        """Get hardware object from uuid"""
        try:
            hardware = Hardware.objects.get(uuid=value)
        except Hardware.DoesNotExist:
            raise serializers.ValidationError("Invalid Hardware UUID")
        else:
            return hardware


class HardwareAssignmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareAssignment
        fields = ["returned_date"]
        extra_kwargs = {"returned_date": {"required": True}}


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
