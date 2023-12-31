from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.models import User

from common.functions import api_get_history
from hardware.functions import get_laptops_assigned
from employee.models import Employee, Department, Designation, Location
from employee.filters import EmployeeAPIFilter
from api.serializers.employee import (
    BaseEmployeeSerializer,
    EmployeeDetailSerializer,
    EmployeeCreateUpdateSerializer,
    DepartmentSerializer,
    DesignationCreateSerializer,
    DesignationSerializer,
    LocationSerializer,
)
from api.serializers.hardware import LaptopV1ListRetrieveSerializer
from api.serializers.common import UserSerializer
from api.custom_pagination import FullResultsSetPagination


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = BaseEmployeeSerializer
    filterset_class = EmployeeAPIFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return EmployeeDetailSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return EmployeeCreateUpdateSerializer
        return BaseEmployeeSerializer


class EmployeeLaptopListView(APIView):
    def get(self, request, **kwargs):
        employee_id = kwargs.get("id", "_")
        laptops = get_laptops_assigned(employee_id)
        result = LaptopV1ListRetrieveSerializer(laptops, many=True)
        return Response(result.data)


class EmployeeHistoryAPIView(APIView):
    def get(self, *args, **kwargs):
        employee_id = kwargs.get("id")
        employee = Employee.objects.get(emp_id=employee_id)
        employee_history = employee.history.all()
        history = api_get_history(employee_history)
        return Response({"employee": employee.emp_name, "history": history})


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
        department = self.request.query_params.get("dept_id")
        if department:
            queryset = queryset.filter(dept_id=department)
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return DesignationCreateSerializer
        return self.serializer_class


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class UserCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        body = request.data
        user = User.objects.create_user(**body)
        return Response(
            {"status": "success", "data": f"{user.username} successfully created"}
        )
