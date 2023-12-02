from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count, Q

from common.functions import api_get_history
from employee.models import Employee
from hardware.models import Laptop, LaptopV2, LaptopBrand, Building
from hardware.functions import api_get_laptop_count_by_value
from api.serializers.hardware import (
    LaptopV1CreateSerializer,
    LaptopV1ListRetrieveSerializer,
    LaptopV2CreateSerializer,
    LaptopV2ListRetrieveSerializer,
    LaptopBrandSerializer,
)
from api.serializers.common import (
    BuildingCreateUpdateSerializer,
    BuildingRetrieveListDeleteSerializer,
)


class LaptopViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["laptop_sr_no", "hardware_id"]

    @action(detail=True, methods=["post"], url_path="return", url_name="return")
    def return_laptop(self, request, pk=None):
        laptop = self.get_object()  # TODO: get remarks and update object
        laptop.emp_id = None
        laptop.save()
        payload = request.data
        employee_id = payload.get("employee_id")
        # TODO: handle employee does not exist
        employee = Employee.objects.get(emp_id=employee_id)
        if not employee.laptop_set.all():
            employee.is_assigned = False
            employee.save()
        return Response({"success": True})

    @action(detail=True, methods=["post"], url_path="assign", url_name="assign")
    def assign_laptop(self, request, pk=None):
        laptop = self.get_object()
        payload = request.data
        employee_id = payload.get("employee_id")
        # TODO: handle employee does not exist
        employee = Employee.objects.get(emp_id=employee_id)
        employee.is_assigned = True
        employee.save()
        laptop.emp_id = employee
        laptop.save()
        return Response({"success": True})

    def get_queryset(self):
        if self.request.version == "2":
            return LaptopV2.objects.all()
        return Laptop.objects.all()

    def get_object(self):
        if self.request.version == "2":
            self.lookup_field = "uuid"
            self.kwargs.update({"uuid": self.kwargs["pk"]})
        return super().get_object()

    def get_serializer_class(self):
        if self.request.version == "2":
            if self.action in ["create", "update", "partial_update"]:
                return LaptopV2CreateSerializer
            return LaptopV2ListRetrieveSerializer
        if self.action in ["create", "update", "partial_update"]:
            return LaptopV1CreateSerializer
        return LaptopV1ListRetrieveSerializer


class LaptopHistoryAPIView(APIView):
    def get(self, *args, **kwargs):
        laptop_id = kwargs.get("id")
        laptop = Laptop.objects.get(id=laptop_id)
        laptop_history = laptop.history.all()
        history = api_get_history(laptop_history)
        return Response({"laptop": laptop.hardware_id, "history": history})


class LaptopBrandViewSet(viewsets.ModelViewSet):
    queryset = LaptopBrand.objects.all()
    serializer_class = LaptopBrandSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return BuildingCreateUpdateSerializer
        return BuildingRetrieveListDeleteSerializer


# Choice Field APIS TODO: move all choices to model
class BaseModelChoicesAPI(APIView):
    model = None
    choice_attr_name = ""
    response_key = ""

    def __init__(self, **kwargs):
        if not all([self.model, self.choice_attr_name, self.response_key]):
            raise AttributeError("Compulsory Attributes Missing")
        super().__init__(**kwargs)

    def get(self, request):
        choices = getattr(self.model, self.choice_attr_name)
        result = [
            {"id": index, "value": choice[0], "label": choice[1]}
            for index, choice in enumerate(choices, start=1)
        ]
        return Response({self.response_key: result})


class LaptopScreenTypeAPI(BaseModelChoicesAPI):
    model = Laptop
    choice_attr_name = "LAPTOP_SCREEN_TYPES"
    response_key = "laptop_screen_types"


class LaptopStatusAPI(BaseModelChoicesAPI):
    model = Laptop
    choice_attr_name = "LAPTOP_STATUSES"
    response_key = "laptop_statuses"


class LaptopOwnerAPI(BaseModelChoicesAPI):
    model = Laptop
    choice_attr_name = "LAPTOP_OWNER_TYPES"
    response_key = "laptop_owner_types"


# Chart APIs
class LaptopChartAPI(APIView):
    chart_label = "# of Laptops"

    def get(self, request):
        response = {
            "laptop_status": {
                "labels": [],
                "datasets": [{"label": self.chart_label, "data": []}],
            },
            "laptop_branch": {
                "labels": [],
                "datasets": [{"label": self.chart_label, "data": []}],
            },
            "laptop_availability": {
                "labels": [],
                "datasets": [{"label": self.chart_label, "data": []}],
            },
            "laptop_age": {
                "labels": [],
                "datasets": [{"label": self.chart_label, "data": []}],
            },
        }
        laptop_status_data = api_get_laptop_count_by_value(value="laptop_status")
        for data in laptop_status_data:
            response["laptop_status"]["labels"].append(data["laptop_status"])
            response["laptop_status"]["datasets"][0]["data"].append(data["total"])

        laptop_branch_data = api_get_laptop_count_by_value(
            value="laptop_branch__location"
        )
        for data in laptop_branch_data:
            response["laptop_branch"]["labels"].append(data["laptop_branch__location"])
            response["laptop_branch"]["datasets"][0]["data"].append(data["total"])

        laptop_assigned_data = Laptop.objects.aggregate(
            unassigned=Count("id", filter=Q(emp_id__isnull=True)),
            assigned=Count("id", filter=Q(emp_id__isnull=False)),
        )
        response["laptop_availability"]["labels"] = list(laptop_assigned_data.keys())
        response["laptop_availability"]["datasets"][0]["data"] = list(
            laptop_assigned_data.values()
        )

        current_year = datetime.now().year
        three_years_before = current_year - 3
        five_years_before = current_year - 5
        all_laptops = Laptop.objects.all()
        laptops_less_than_year = all_laptops.filter(
            laptop_date_purchased__year=current_year  # = 2023
        ).count()
        laptops_between_year_and_three = all_laptops.filter(
            laptop_date_purchased__year__gte=three_years_before,
            laptop_date_purchased__year__lt=current_year,
        ).count()
        laptops_between_three_and_five = all_laptops.filter(
            laptop_date_purchased__year__gte=five_years_before,
            laptop_date_purchased__year__lt=three_years_before,
        ).count()
        laptops_greater_than_five = all_laptops.filter(
            laptop_date_purchased__year__lt=five_years_before
        ).count()
        response["laptop_age"]["labels"] = ["< 1Y", "1-3Y", "3-5Y", ">5Y"]
        response["laptop_age"]["datasets"][0]["data"] = [
            laptops_less_than_year,
            laptops_between_year_and_three,
            laptops_between_three_and_five,
            laptops_greater_than_five,
        ]
        return Response(response)
