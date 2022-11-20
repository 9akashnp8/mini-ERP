from datetime import date

from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    department_id = models.AutoField(primary_key=True, editable=False)
    dept_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.dept_name

class Designation(models.Model):
    dept_id = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    designation_id = models.AutoField(primary_key=True, editable=False)
    designation = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.designation

class Location(models.Model):
    location_id = models.AutoField(primary_key=True, editable=False)
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.location

class Employee(models.Model):
    EMPLOYEE_STATUS = (
        ('Active', 'Active'),
        ('InActive', 'Inactive'),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    emp_id = models.AutoField(primary_key=True, editable=False)
    lk_emp_id = models.CharField(null=True, blank=False, unique=True, max_length=15)
    dept_id = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    desig_id = models.ForeignKey(Designation,  null=True, on_delete=models.SET_NULL)
    emp_name = models.CharField(max_length=100)
    emp_email = models.CharField(max_length=100)
    emp_phone = models.CharField(max_length=10, null=True, blank=True)
    emp_status = models.CharField(max_length=10, choices=EMPLOYEE_STATUS, default='Active')
    loc_id = models.ForeignKey(Location,  null=True, on_delete=models.SET_NULL)
    emp_date_joined = models.DateField(default=date.today)
    emp_date_exited = models.DateField(null=True, blank=True)
    emp_date_created = models.DateField(auto_now_add=True)
    is_assigned = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        if self.emp_name == None:
            return "NAME IS NULL"
        return self.emp_name

class EmployeeAppSetting(models.Model):
    org_emp_id_prefix = models.CharField(max_length=10)
    
    def __str__(self):
        return self.org_emp_id_prefix