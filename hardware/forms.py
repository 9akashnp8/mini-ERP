from django.forms import DateInput, ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from psycopg2 import Date
from .models import Designation, Employee, Laptop

class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user', 'is_assigned']
        widgets = {
            'emp_date_joined': DateInput(attrs={'type':'date'}),
            'emp_date_exited': DateInput(attrs={'type':'date'})
        }
        labels = {
            'lk_emp_id': 'Employee ID',
            'dept_id': 'Department',
            'desig_id': 'Designation',
            'emp_name': 'Name',
            'emp_email': 'Email ID',
            'emp_phone': 'Mobile Number',
            'emp_status': 'Employee Status',
            'loc_id': 'Branch',
            'emp_date_joined': 'Date of Joining',
            'emp_date_exited': 'Date of Exit',
            'is_assigned': 'Laptop Assigned?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Department-Designation auto dependant dropdown
        self.fields['desig_id'].queryset = Designation.objects.none()
        if 'dept_id' in self.data:
            try:
                dept_id = int(self.data.get('dept_id'))
                self.fields['desig_id'].queryset = Designation.objects.filter(dept_id=dept_id).order_by('designation')
            except (ValueError, TypeError):
                pass
        elif self.instance.emp_id:
            self.fields['desig_id'].queryset = Designation.objects.filter(dept_id=self.instance.dept_id).order_by('designation')
        
        #Custom class names for form fields styling
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'employee-form-fields'})
    
    def clean(self):
        '''Overide clean method to check if a 'User' object with same email
        ID exists, raise a custom validation error if so.
        '''
        email = self.cleaned_data['emp_email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email ID is already being used for an ERP User. Please use another email")

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
            self.fields[key].widget.attrs.update({'class': 'laptop-form-fields'})
        
        self.fields['hardware_id'].widget.attrs.update({'placeholder': 'Hardware ID is auto-generated.'})

class LaptopAssignmentForm(ModelForm):
    class Meta:
        model = Laptop
        fields = ['emp_id', 'laptop_sr_no']

class OnboardEmployeeAddForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user',]

# class EmployeeExitFormLaptopImage(ModelForm):
#     class Meta:
#         model = LaptopMedia
#         fields = ['media']
    
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