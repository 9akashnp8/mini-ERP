from django.forms import DateInput, ModelForm
from .models import Employee, Laptop

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