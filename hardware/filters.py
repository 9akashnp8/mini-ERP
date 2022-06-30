import django_filters
from django_filters import CharFilter, ChoiceFilter
from .models import *

class EmployeeFilter(django_filters.FilterSet):
    choices = (
    (True, "Assigned"),
    (False, "Not Assigned"))

    is_assigned = ChoiceFilter(choices=choices)
    name_contains = CharFilter(field_name='emp_name', lookup_expr='icontains')
    class Meta:
        model = Employee
        fields = ['name_contains', 'dept_id', 'desig_id', 'loc_id', 'emp_status', 'is_assigned']

class LaptopFilter(django_filters.FilterSet):
    class Meta:
        model = Laptop
        fields = '__all__'

class ExitEmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ['lk_emp_id',]

    def __init__(self, *args, **kwargs):
        super(ExitEmployeeFilter, self).__init__(*args, **kwargs)
        self.filters['lk_emp_id'].label = "Lakshya Employee ID"

