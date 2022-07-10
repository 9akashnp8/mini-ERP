import django_filters
from django_filters import CharFilter, ChoiceFilter
from .models import *

class EmployeeFilter(django_filters.FilterSet):

    IS_ASSIGNED_CHOICES = (
        (True, "Assigned"),
        (False, "Not Assigned")
    )

    EMPLOYEEE_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('InActive', 'Inactive'),
    )

    is_assigned = ChoiceFilter(choices=IS_ASSIGNED_CHOICES, empty_label="Select Laptop Status")
    name_contains = CharFilter(field_name='emp_name', lookup_expr='icontains')
    emp_status = ChoiceFilter(choices=EMPLOYEEE_STATUS_CHOICES, empty_label="Select Employee Status")
    
    class Meta:
        model = Employee
        fields = ['lk_emp_id', 'name_contains', 'dept_id', 'desig_id', 'loc_id', 'emp_status', 'is_assigned']
    
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):

        super(EmployeeFilter, self).__init__(data, queryset, request=request, prefix=prefix)

        #For Custom CSS        
        for field in self.form.fields:
            self.form.fields[field].widget.attrs.update({'class': 'employee-filter-fields'})
        
        #For Placeholders & Empty Labels
        self.form.fields['dept_id'].empty_label = "Select Department"
        self.form.fields['desig_id'].empty_label = "Select Designation"
        self.form.fields['loc_id'].empty_label = "Select Location"
        self.form.fields['lk_emp_id'].widget.attrs.update({'placeholder': 'Employee ID'})
        self.form.fields['name_contains'].widget.attrs.update({'placeholder': 'Employee Name'})
          

class LaptopFilter(django_filters.FilterSet):
    LAPTOP_STATUS_CHOICES = (
        ('Working', 'Working'),
        ('Repair', 'Repair'),
        ('Replace', 'Replace'),
    )

    laptop_status = ChoiceFilter(choices=LAPTOP_STATUS_CHOICES, empty_label='Select Condition')
    class Meta:
        model = Laptop
        fields = ['laptop_sr_no', 'hardware_id', 'brand', 'laptop_status', 'laptop_branch']
    
    def __init__(self, data=None, queryset=None, request=None, prefix=None):

        super(LaptopFilter, self).__init__(data, queryset, request=request, prefix=prefix)
        
        #Custom CSS for styling
        for form in self.form.fields:
            self.form.fields[form].widget.attrs.update({'class': 'laptop-filter-fields'})
        
        #Placeholders
        self.form.fields['laptop_sr_no'].widget.attrs.update({'placeholder': 'Serial No.'})
        self.form.fields['hardware_id'].widget.attrs.update({'placeholder': 'Hardware ID'})
        self.form.fields['brand'].empty_label = 'Select Brand'
        self.form.fields['laptop_branch'].empty_label = 'Select Branch'


class ExitEmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = ['lk_emp_id',]

    def __init__(self, *args, **kwargs):
        super(ExitEmployeeFilter, self).__init__(*args, **kwargs)
        self.filters['lk_emp_id'].label = "Lakshya Employee ID"

