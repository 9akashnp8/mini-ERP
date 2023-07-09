from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from common.functions import api_get_history
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
    EmployeeCreateSerializer,
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
        elif self.action == 'create':
            return EmployeeCreateSerializer
        return BaseEmployeeSerializer


class EmployeeHistoryAPIView(APIView):

    def get(self, *args, **kwargs):
        employee_id = kwargs.get('id')
        employee = Employee.objects.get(emp_id=employee_id)
        employee_history = employee.history.all()
        history = api_get_history(employee_history)
        return Response({
            "employee": employee.emp_name,
            "history": history
        })


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
        if department:
            queryset = queryset.filter(dept_id=department)
        return queryset


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
