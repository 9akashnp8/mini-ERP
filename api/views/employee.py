from rest_framework import viewsets

from employee.models import (
    Employee,
    Department,
    Designation,
    Location
)
from employee.filters import EmployeeAPIFilter
from api.serializers import (
    BaseEmployeeSerializer,
    EmployeeDetailSerializer,
    DepartmentSerializer,
    DesignationSerializer,
    LocationSerializer,
)
from api.custom_pagination import FullResultsSetPagination

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = BaseEmployeeSerializer
    filterset_class = EmployeeAPIFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return BaseEmployeeSerializer
        

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