from django.forms import DateInput, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Designation, Employee, Hardware, Laptop

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user', 'laptop_assiged',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['desig_id'].queryset = Designation.objects.all()

class LaptopForm(ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'
        widgets = {
            'laptop_date_purchased': DateInput(),
            'laptop_date_sold': DateInput()
        }

class LaptopAssignmentForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['laptop_assiged',]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        added_emp = Employee.objects.last()
        self.fields['laptop_assiged'].queryset = Laptop.objects.filter(laptop_location=added_emp.loc_id)

class CreateUserForm(UserCreationForm, EmployeeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']