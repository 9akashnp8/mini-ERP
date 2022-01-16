from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class Department(models.Model):
    department_id = models.AutoField(primary_key=True, editable=False)
    dept_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.dept_name

class Designation(models.Model):
    dept_id = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    designation_id = models.AutoField(primary_key=True, editable=False)
    designation = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.designation

class User(models.Model):
    USER_TYPES = (
        ('User', 'User'),
        ('Staff', 'Staff'),
    )
    user_id = models.AutoField(primary_key=True, editable=False)
    user_name = models.CharField(max_length=20, null=True, unique=True)
    user_type = models.CharField(max_length=10, null=True, choices=USER_TYPES)
    
    def __str__(self):
        return self.user_name

class Location(models.Model):
    location_id = models.AutoField(primary_key=True, editable=False)
    location = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.location

class Employee(models.Model):
    EMPLOYEE_STATUS = (
        ('Active', 'Active'),
        ('InActive', 'Inactive'),
    )
    emp_id = models.AutoField(primary_key=True, editable=False)
    dept_id = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    desig_id = models.ForeignKey(Designation, null=True, on_delete=models.SET_NULL)
    username = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    emp_name = models.CharField(max_length=100, null=True)
    emp_email = models.CharField(max_length=100, null=True)
    emp_phone = models.IntegerField(null=True)
    emp_status = models.CharField(max_length=10, null=True, choices=EMPLOYEE_STATUS)
    loc_id = models.ForeignKey(Location, null=True, blank=False, on_delete=models.SET_NULL)
    emp_date_joined = models.DateField
    emp_date_exited = models.DateField
    emp_date_created = models.DateField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.emp_name
