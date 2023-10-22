from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers

from employee.models import Department, Designation, Employee, Location
from hardware.models import Building, Laptop, LaptopBrand
from finance.models import Payment
from common.models import EmployeeAppSetting, HardwareAppSetting


# Employee Serializers
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):

    dept_id = DepartmentSerializer()

    class Meta:
        model = Designation
        fields = '__all__'


class DesignationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email_address'
            'username',
        ]


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class BaseEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        exclude = ['user']
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
        email = validated_data.get('emp_email')
        try:
            # move default password to settings
            user = User.objects.create_user(email, email, 'lakshya123')
        except IntegrityError:
            raise serializers.ValidationError({
                "emp_email": ["User with username/email already exists"]
            })
        else:
            employee = super().create({**validated_data, 'user': user})
            return employee

    def update(self, instance, validated_data):
        # TODO: validate if user with email exists,
        # TODO: update email of related user
        return super().update(instance, validated_data)


# Hardware Serializers
class LaptopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Laptop
        fields = '__all__'
        depth = 1


class LaptopCreateSerializer(LaptopSerializer):

    class Meta(LaptopSerializer.Meta):
        depth = 0


class LaptopBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = LaptopBrand
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):

    location = LocationSerializer()

    class Meta:
        model = Building
        fields = '__all__'

class BuildingRetrieveListDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Building
        fields = '__all__'
        depth = 1


class BuildingCreateUpdateSerializer(serializers.ModelSerializer):

    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all()
    )

    class Meta:
        model = Building
        fields = '__all__'

# Finance Serializers
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'


class EmployeeAppSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeAppSetting
        fields = '__all__'


class HardwareAppSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = HardwareAppSetting
        fields = '__all__'
