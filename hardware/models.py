from django.db import models
from simple_history.models import HistoricalRecords
from datetime import date

#Models for Employee side of the app
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

#Models for the Laptop side of the app
class LaptopBrand(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    brand_name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.brand_name

class LaptopModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    brand_id = models.ForeignKey(LaptopBrand, null=True, on_delete=models.SET_NULL)
    model_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.model_name

class LaptopMedia(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    media = models.ImageField(upload_to='uploads/')

class Laptop(models.Model):
    LAPTOP_STATUSES = (
        ('Working', 'Working'),
        ('Repair', 'Repair'),
        ('Replace', 'Replace'),
    )
    id = models.AutoField(primary_key=True, editable=False)
    hardware_id = models.CharField(max_length=50, null=True, default=None, blank=True, unique=True)
    laptop_sr_no = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(LaptopBrand, null=True, on_delete=models.SET_NULL)
    model = models.ForeignKey(LaptopModel, null=True, on_delete=models.SET_NULL)
    media = models.ForeignKey(LaptopMedia, null=True, on_delete=models.SET_NULL)
    laptop_status = models.CharField(max_length=20, null=True, choices=LAPTOP_STATUSES)
    laptop_date_purchased = models.DateField(null=True)
    laptop_date_sold = models.DateField(null=True, blank=True)
    laptop_date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.hardware_id

    def save(self,*args, **kwargs):   
        if not self.hardware_id:
            prefix = 'LAK-LAP'
            id = Laptop.objects.count()+1
            self.hardware_id = prefix+'-'+'{0:04d}'.format(id)
        super(Laptop, self).save(*args, **kwargs)

    @property
    def laptop_age(self):
        today = date.today()
        age = today - self.laptop_date_purchased
        age_stripped = str(age).split(",", 1)[0]
        return age_stripped

#Model linking the Employee to the various hardwares (Eg: Laptops, Tablets)
class Hardware(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    emp_id = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
    hardware_id = models.ForeignKey(Laptop, null=True, on_delete=models.SET_NULL)
