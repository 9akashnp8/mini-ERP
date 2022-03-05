from tkinter.tix import Select
from django.forms import DateInput, ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Designation, Employee, Hardware, Laptop, LaptopMedia

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user',]
    
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
        model = Laptop
        fields = ['emp_id', 'laptop_sr_no']

class OnboardEmployeeAddForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user',]

class EmployeeExitFormLaptopImage(ModelForm):
    class Meta:
        model = LaptopMedia
        fields = ['media']
    
class EmployeeExitFormLaptop(ModelForm):
    class Meta:
        model = Laptop
        fields = [ 'laptop_date_returned', 'laptop_return_remarks',]
        widgets = {
            'laptop_date_returned': DateInput(),
        }

class CreateUserForm(UserCreationForm, EmployeeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']