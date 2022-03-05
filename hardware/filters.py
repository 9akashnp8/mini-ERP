import django_filters
from django_filters import CharFilter
from .models import *

class EmployeeFilter(django_filters.FilterSet):
    name_contains = CharFilter(field_name='emp_name', lookup_expr='icontains')
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['username', 'emp_date_created', 'emp_name', 'profilePic']

class ExitEmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ['lk_emp_id',]

    def __init__(self, *args, **kwargs):
        super(ExitEmployeeFilter, self).__init__(*args, **kwargs)
        self.filters['lk_emp_id'].label = "Lakshya Employee ID"

