from rest_framework import serializers
from django.contrib.auth.models import User

from employee.models import Department, Designation, Employee, Location

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):

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

    dept_id = serializers.StringRelatedField()
    desig_id = serializers.StringRelatedField()
    loc_id = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = '__all__'
