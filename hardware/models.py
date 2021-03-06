from uuid import uuid4
from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from datetime import date
import os

#Models for Employee side of the app
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

class Userz(models.Model):
    #Delete this
    USER_TYPES = (
        ('User', 'User'),
        ('Staff', 'Staff'),
    )
    user_id = models.AutoField(primary_key=True, editable=False)
    user_name = models.CharField(max_length=20, null=True, unique=True)
    user_type = models.CharField(max_length=20, null=True, choices=USER_TYPES)
    
    def __str__(self):
        return self.user_name

class Location(models.Model):
    location_id = models.AutoField(primary_key=True, editable=False)
    location = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.location

class Building(models.Model):
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    building = models.CharField(max_length=50)

    def __str__(self):
        return self.building

#Models for the Laptop side of the app
class LaptopBrand(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    brand_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.brand_name

class LaptopModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    brand_id = models.ForeignKey(LaptopBrand, null=True, on_delete=models.SET_NULL)
    model_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.model_name

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

    def save(self,*args, **kwargs):  
        laptop_status = Laptop.objects.filter(emp_id=self.emp_id).exists()
        if laptop_status:
            self.is_assigned = True
        else:
            self.is_assigned = False
        super(Employee, self).save(*args, **kwargs)

class Laptop(models.Model):
    LAPTOP_STATUSES = (
        ('Working', 'Working'),
        ('Repair', 'Repair'),
        ('Replace', 'Replace'),
    )

    id = models.AutoField(primary_key=True, editable=False)
    hardware_id = models.CharField(max_length=50, null=True, default=None, blank=True, unique=True)
    emp_id = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    laptop_sr_no = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(LaptopBrand, null=True, on_delete=models.SET_NULL)
    processor = models.CharField(max_length=15, default='i3 11th gen')
    ram_capacity = models.CharField(max_length=5, default='8GB')
    storage_capacity = models.CharField(max_length=10, default='512GB')
    laptop_status = models.CharField(max_length=20, null=True, choices=LAPTOP_STATUSES, default="Working")
    laptop_branch = models.ForeignKey(Location, null=True, blank=False, on_delete=models.SET_NULL)
    laptop_building = models.ForeignKey(Building, null=True, on_delete=models.SET_NULL)
    laptop_date_purchased = models.DateField(null=True)
    laptop_date_sold = models.DateField(null=True, blank=True)
    laptop_date_created = models.DateField(auto_now_add=True)
    laptop_date_returned = models.DateField(null=True, blank=True)
    laptop_return_remarks = models.TextField(max_length=500, null=True, blank=True)
    history = HistoricalRecords()

    
    def __str__(self):
        return self.hardware_id 

    @property
    def laptop_age(self):
        today = date.today()
        age = today - self.laptop_date_purchased
        age_stripped = str(age).split(",", 1)[0]
        if age_stripped != "0:00:00":
            if age_stripped == "1 day":
                return age_stripped
            else:
                age_int = int(age_stripped[:-5])
                if age_int >= 365:
                    years = round(age_int / 365, 1)
                    return f"{years} years"
                elif age_int >= 30 and age_int <= 365:
                    months = round(age_int / 30, 1)
                    return f"{months} months"
                elif age_int <= 30:
                    return f"{age_int} days"
        else:
            return "0 days"


def path_and_rename(instance, filename):
    upload_to='images/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}-for-{}.{}'.format(date.today(), instance.laptop_id, ext)
    return os.path.join(upload_to, filename)

#Model linking the Employee to the various hardwares (Eg: Laptops, Tablets)
class Hardware(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    emp_id = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    hardware_id = models.ForeignKey(Laptop, null=True, on_delete=models.SET_NULL)
