from django_filters import rest_framework as filters

from hardware.models import HardwareAssignment


class HardwareAssignmentFilter(filters.FilterSet):
    hardware = filters.NumberFilter(field_name="hardware")
    employee = filters.NumberFilter(field_name="employee")
    is_free = filters.BooleanFilter(field_name="returned_date", lookup_expr="isnull")

    class Meta:
        model = HardwareAssignment
        fields = ["hardware", "employee"]
