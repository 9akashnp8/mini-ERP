from django.forms import DateInput, ModelForm, ChoiceField, CharField, Textarea
from django import forms

from hardware.models import Laptop, HardwareAppSetting
from employee.models import Employee

# Helpers
def string_to_choice_tuple(string):
    list_from_string = string.split(",")
    final_list_for_tuple = []
    for item in list_from_string:
        temp_list = []
        temp_list.append(item)
        item_tuple = tuple(temp_list*2)
        final_list_for_tuple.append(item_tuple)
    return tuple(final_list_for_tuple)

# Forms
class LaptopForm(ModelForm):
    screen_size = ChoiceField()
    laptop_rental_vendor = ChoiceField()

    class Meta:
        model = Laptop
        fields = '__all__'
        widgets = {
            'laptop_date_purchased': DateInput(attrs={'type':'date'}),
            'laptop_date_sold': DateInput(attrs={'type':'date'}),
            'laptop_date_returned': DateInput(attrs={'type':'date'})
        }
        labels = {
            'hardware_id': 'Hardware ID',
            'emp_id': 'Employee Assigned to',
            'laptop_sr_no': 'Serial Number',
            'brand': 'Brand',
            'processor': 'Processor',
            'ram_capacity': 'RAM',
            'storage_capacity': 'Storage',
            'laptop_status': 'Laptop Status',
            'laptop_branch': 'Branch (Location)',
            'laptop_building': 'Building (Location)',
            'laptop_date_purchased': 'Purchase Date',
            'laptop_date_sold': 'Date Sold',
            'laptop_date_returned': 'Date Returned',
            'laptop_return_remarks': 'Remarks'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set choices to be from the same set it Hardware Settings.
        try:
            hardware_settings = HardwareAppSetting.objects.get(id=1)
            self.fields['screen_size'].choices = string_to_choice_tuple(hardware_settings.laptop_screen_sizes)
            self.fields['laptop_rental_vendor'].choices = string_to_choice_tuple(hardware_settings.laptop_rental_vendors)
            self.fields['processor'].initial = hardware_settings.laptop_default_processor
            self.fields['ram_capacity'].initial = hardware_settings.laptop_default_ram
            self.fields['storage_capacity'].initial = hardware_settings.laptop_default_storage
        except HardwareAppSetting.DoesNotExist:
            self.fields['screen_size'].choices = (('14', '14 inch'), ('15', '15 inch'))
            self.fields['laptop_rental_vendor'].choices = (('V1', 'Vendor 1'), ('V2', 'Vendor 2'))
            self.fields['processor'].initial = 'i3 12th gen'
            self.fields['ram_capacity'].initial = '8GB'
            self.fields['storage_capacity'].initial = '512GB SSD'

        #Setting Custom class names for form field styling
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'laptop-form-fields form-fields'})
        
        #Placeholder text for Hardware ID
        self.fields['hardware_id'].widget.attrs.update({'placeholder': 'Hardware ID is auto-generated.'}) 

class LaptopReturnForm(forms.Form):
    laptop_date_returned = forms.DateField(
        widget=DateInput(
            attrs={'type':'date'}
        )
    )
    laptop_return_remarks = forms.CharField(
        max_length=200,
        widget=Textarea(
            attrs={'rows': '5', 'cols': '2'}
        )
    )
    returning_laptop = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'return-form-fields form-fields'})
            self.fields[field].required = True

class HardwareAppSettingsForm(ModelForm):
    class Meta:
        model = HardwareAppSetting
        fields = '__all__'
        labels = {
            'laptop_hardware_id_prefix': 'Hardware ID Prefix',
            'laptop_default_processor': 'Default Laptop Processor',
            'laptop_default_ram': 'Default Laptop RAM',
            'laptop_default_storage': 'Default Laptop Storage',
            'laptop_screen_sizes': 'Available Laptop Screen Sizes',
            'laptop_rental_vendors': 'Available Laptop Rental Vendors'
        }
    
    def __init__(self, *args, **kwargs):
        super(HardwareAppSettingsForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'laptop-form-fields form-fields'})
