from django_filters import rest_framework as filters

from hardware.models import HardwareAssignment, Hardware


class HardwareFilter(filters.FilterSet):
    is_free = filters.BooleanFilter(method="filter_is_free")
    type = filters.NumberFilter(field_name="type")

    def filter_is_free(self, queryset, field_name, value):
        if value is True:
            return queryset.get_available_hardware()
        return queryset

    class Meta:
        model = Hardware
        fields = ["type"]


class HardwareAssignmentFilter(filters.FilterSet):
    hardware = filters.NumberFilter(field_name="hardware")
    employee = filters.NumberFilter(field_name="employee")
    is_free = filters.BooleanFilter(field_name="returned_date", lookup_expr="isnull")

    class Meta:
        model = HardwareAssignment
        fields = ["hardware", "employee"]
