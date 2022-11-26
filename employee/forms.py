from django.forms import ModelForm, DateInput, ValidationError
from django.contrib.auth.models import User

from .models import Employee, Designation, EmployeeAppSetting
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
        # employee_app_settings = EmployeeAppSetting.objects.get(id=1)
        self.fields['lk_emp_id'].initial = 'LAK-IND-' # employee_app_settings.org_emp_id_prefix

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

class EmployeeAppSettingsForm(HardwareAppSettingsForm):
    class Meta:
        model = Employee
        fields = '__all__'
        labels = {}