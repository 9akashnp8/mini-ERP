from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers

from employee.models import Department, Designation, Employee, Location
from hardware.models import Building, Laptop, LaptopBrand
from finance.models import Payment


# Employee Serializers
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class DesignationSerializer(serializers.ModelSerializer):

    dept_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )

    class Meta:
        model = Designation
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email'
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


class EmployeeCreateSerializer(BaseEmployeeSerializer):

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
            employee = Employee.objects.create(user=user, **validated_data)
            return employee


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

    location = serializers.StringRelatedField()

    class Meta:
        model = Building
        fields = '__all__'


# Finance Serializers
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
