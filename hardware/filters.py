import django_filters
from django_filters import ChoiceFilter
from .models import Laptop      

class LaptopFilter(django_filters.FilterSet):
    LAPTOP_STATUS_CHOICES = (
        ('Working', 'Working'),
        ('Repair', 'Repair'),
        ('Replace', 'Replace'),
    )
    laptop_status = ChoiceFilter(choices=LAPTOP_STATUS_CHOICES, empty_label='Select Condition')

    LAPTOP_CHOICES = (
        (True, 'Available'),
        (False, 'Assigned')
    )
    laptop_availability = ChoiceFilter(choices=LAPTOP_CHOICES, method='filter_laptop_availability', empty_label='Select Availability')

    def filter_laptop_availability(self, queryset, name, value):
        if value == "True":
            return queryset.filter(emp_id__isnull=True)
        else:
            return queryset.filter(emp_id__isnull=False)

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

