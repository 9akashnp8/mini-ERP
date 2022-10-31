from dataclasses import fields
from rest_framework import serializers
from django.contrib.auth.models import User

from employee.models import Department, Designation, Employee, Location
from hardware.models import Building, Laptop, LaptopBrand
from finance.models import Payment

# Employee Serializers
class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    
    dept_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

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

class EmployeeSerializer(serializers.ModelSerializer):

    dept_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    desig_id = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all())
    loc_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = '__all__'

# Hardware Serializers
class LaptopSerializer(serializers.ModelSerializer):

    brand = serializers.StringRelatedField()
    laptop_branch = serializers.StringRelatedField()
    laptop_building = serializers.StringRelatedField()
    emp_id = serializers.ReadOnlyField(source='emp_id.lk_emp_id')

    class Meta:
        model = Laptop
        fields = '__all__'

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