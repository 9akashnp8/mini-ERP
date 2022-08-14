from datetime import date
import os

from django.db import models
from simple_history.models import HistoricalRecords
from employee.models import Location, Employee

#Models for Employee side of the app
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
