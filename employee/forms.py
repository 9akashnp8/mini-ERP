from django.forms import ModelForm, DateInput, ValidationError
from django.contrib.auth.models import User
from django.db.utils import OperationalError

from .models import Employee, Department, Designation, EmployeeAppSetting
from hardware.forms import HardwareAppSettingsForm

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
        super(EmployeeForm, self).__init__(*args, **kwargs)

        # Settings from EmployeeAppSettings
        try:
            employee_app_settings = EmployeeAppSetting.objects.get(id=1)
            self.fields['lk_emp_id'].initial = employee_app_settings.org_emp_id_prefix
        except (OperationalError, EmployeeAppSetting.DoesNotExist):
            pass

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
            self.fields[key].widget.attrs.update({'class': 'employee-form-fields form-fields'})
    
    def clean(self):
        '''Overide clean method to check if a 'User' object with same email
        ID exists, raise a custom validation error if so.
        '''
        if self.instance.pk is None:
            email = self.cleaned_data['emp_email']
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email ID is already being used for an ERP User. Please use another email")

class EmployeeAppSettingsForm(ModelForm):
    class Meta:
        model = EmployeeAppSetting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs.update({'class': 'laptop-form-fields form-fields'})

class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']

    def clean_dept_name(self):
        dept_name = self.cleaned_data['dept_name']
        if Department.objects.filter(dept_name__iexact=dept_name).exists():
            raise ValidationError(
                ('Department with name "%(dept_name)s" already exists.'),
                code='invalid',
                params={'dept_name': dept_name},
            )
        return dept_name