from django.forms import DateInput, ModelForm
from .models import Employee, Hardware, Laptop

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class LaptopForm(ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'
        widgets = {
            'laptop_date_purchased': DateInput(),
            'laptop_date_sold': DateInput()
        }

class HardwareAssignmentForm(ModelForm):
    class Meta:
        model = Hardware
        fields = '__all__'