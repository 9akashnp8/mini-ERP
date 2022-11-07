from django.forms import DateInput, ModelForm

from hardware.models import Laptop, HardwareAppSettings
from employee.models import Employee

class LaptopForm(ModelForm):

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

        #Setting Custom class names for form field styling
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'laptop-form-fields form-fields'})
        
        #Placeholder text for Hardware ID
        self.fields['hardware_id'].widget.attrs.update({'placeholder': 'Hardware ID is auto-generated.'}) 

class LaptopReturnForm(ModelForm):

    class Meta:
        model = Laptop
        fields = ['laptop_date_returned', 'laptop_return_remarks',]
        widgets = {
            'laptop_date_returned': DateInput(attrs={'type':'date'})
        }
        labels = {
            'laptop_date_returned': 'Returning Date',
            'laptop_return_remarks': 'Remarks'
        }
    
    def __init__(self, *args, **kwargs):

        self.returning = None

        super(LaptopReturnForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'return-form-fields form-fields'})
            self.fields[field].required = True
    
    def save(self, *args, **kwargs):

        self.returning = kwargs.pop('returning', None)
        if self.returning:

            count_of_laptops_assigned = Laptop.objects.filter(emp_id=self.instance.emp_id.emp_id).count()

            if count_of_laptops_assigned > 1:

                self.instance.emp_id = None
                self.instance.save()
            
            elif count_of_laptops_assigned == 1:
                        
                employee = Employee.objects.get(emp_id=self.instance.emp_id.emp_id)
                employee.is_assigned = False
                employee.save()
                
                self.instance.emp_id = None
                self.instance.save()

            else:
                
                pass
        
        return super(LaptopReturnForm, self).save(*args, **kwargs)

class HardwareAppSettingsForm(ModelForm):

    class Meta:
        model = HardwareAppSettings
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
