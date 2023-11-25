from rest_framework import serializers
from django.db.utils import IntegrityError


from .hardware import LaptopSerializer
from employee.models import (
    Department,
    Designation,
    Location,
    Employee,
)
from django.contrib.auth.models import User
from hardware.models import Laptop


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DesignationSerializer(serializers.ModelSerializer):
    dept_id = DepartmentSerializer()

    class Meta:
        model = Designation
        fields = "__all__"


class DesignationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class BaseEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ["user"]
        depth = 1


class EmployeeDetailSerializer(BaseEmployeeSerializer):
    laptops = serializers.SerializerMethodField()

    def get_laptops(self, employee):
        laptops = Laptop.objects.filter(emp_id=employee.emp_id)
        serializer = LaptopSerializer(laptops, many=True)
        return serializer.data


class EmployeeCreateUpdateSerializer(BaseEmployeeSerializer):
    class Meta(BaseEmployeeSerializer.Meta):
        depth = 0

    def create(self, validated_data):
        """
        create and link corresponding User object to Employee.
        """
        email = validated_data.get("emp_email")
        try:
            # move default password to settings
            user = User.objects.create_user(email, email, "lakshya123")
        except IntegrityError:
            raise serializers.ValidationError(
                {"emp_email": ["User with username/email already exists"]}
            )
        else:
            employee = super().create({**validated_data, "user": user})
            return employee

    def update(self, instance, validated_data):
        # TODO: validate if user with email exists,
        # TODO: update email of related user
        return super().update(instance, validated_data)
