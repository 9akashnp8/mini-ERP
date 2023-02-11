from rest_framework import viewsets

from employee.models import (
    Employee,
    Department,
    Designation,
    Location
)
from api.serializers import (
    EmployeeSerializer,
    DepartmentSerializer,
    DesignationSerializer,
    LocationSerializer,
)
from api.custom_pagination import FullResultsSetPagination

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    pagination_class = FullResultsSetPagination

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    pagination_class = FullResultsSetPagination

    def get_queryset(self):
        # Capture department from query parameters
        queryset = Designation.objects.all()
        department = self.request.query_params.get('dept_id')
        if department is not None:
            queryset = queryset.filter(dept_id=department)
        return queryset

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer