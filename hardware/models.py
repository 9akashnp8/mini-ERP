from collections.abc import Collection
import os
from typing import Any
import uuid
from datetime import date, datetime

from django.db import models, transaction
from django.db.models import Q
from django.core.exceptions import ValidationError
from simple_history.models import HistoricalRecords

from common.functions import generate_unique_identifier
from employee.models import Location, Employee


class Building(models.Model):
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    building = models.CharField(max_length=50)

    def __str__(self):
        return self.building


class HardwareAppSetting(models.Model):
    laptop_hardware_id_prefix = models.CharField(max_length=30)
    laptop_default_processor = models.CharField(max_length=30)
    laptop_default_ram = models.CharField(max_length=10)
    laptop_default_storage = models.CharField(max_length=10)
    laptop_screen_sizes = models.CharField(max_length=100)
    laptop_screen_sizes = models.CharField(max_length=100)
    laptop_rental_vendors = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)


# Models for the Laptop side of the app
class LaptopBrand(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    brand_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.brand_name


class Laptop(models.Model):
    LAPTOP_STATUSES = (
        ("Working", "Working"),
        ("Repair", "Repair"),
        ("Replace", "Replace"),
    )

    LAPTOP_OWNER_TYPES = (
        ("CO", "Company Owned"),
        ("Rental", "Rental"),
    )

    LAPTOP_SCREEN_TYPES = (("Touch", "Touch"), ("Non-Touch", "Non-Touch"))

    id = models.AutoField(primary_key=True, editable=False)
    hardware_id = models.CharField(
        max_length=50, null=True, default=None, blank=True, unique=True
    )
    emp_id = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.SET_NULL
    )
    laptop_sr_no = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(LaptopBrand, null=True, on_delete=models.SET_NULL)
    processor = models.CharField(max_length=15)
    ram_capacity = models.CharField(max_length=5)
    storage_capacity = models.CharField(max_length=10)
    screen_size = models.CharField(max_length=15)
    screen_type = models.CharField(
        max_length=15, null=True, choices=LAPTOP_SCREEN_TYPES, default="Non-Touch"
    )
    laptop_owner_type = models.CharField(
        max_length=30, null=True, choices=LAPTOP_OWNER_TYPES, default="Rental"
    )
    laptop_rental_vendor = models.CharField(max_length=50, null=True, blank=True)
    laptop_status = models.CharField(
        max_length=20, null=True, choices=LAPTOP_STATUSES, default="Working"
    )
    laptop_branch = models.ForeignKey(
        Location, null=True, blank=False, on_delete=models.SET_NULL
    )
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
        if self.laptop_date_purchased:
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
        else:
            return "unknown"

    class Meta:
        permissions = [("can_return_laptop", "Can process laptop return requests")]


def path_and_rename(instance, filename):
    upload_to = "images/"
    ext = filename.split(".")[-1]
    if instance.pk:
        filename = "{}.{}".format(instance.pk, ext)
    else:
        filename = "{}-for-{}.{}".format(date.today(), instance.laptop_id, ext)
    return os.path.join(upload_to, filename)


class HardwareType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HardwareOwner(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class HardwareCondition(models.Model):
    condition = models.CharField(max_length=255)

    def __str__(self):
        return self.condition


class HardwareQuerySet(models.QuerySet):
    def get_available_hardware(self):
        """
        Filter Hardware that have no assignement records OR that have been
        returned i.e., Filter hardware that is available.
        """
        q1 = Q(employees_assigned__isnull=True)
        q2 = Q(employees_assigned__returned_date__isnull=False)
        q3 = ~Q(employees_assigned__returned_date__isnull=True)
        return self.filter(q1 | q2 & q3).distinct()

    def get_assigned_hardware(self):
        """
        Filter Hardware that have been assigned to employee(s)
        """
        query = Q(employees_assigned__isnull=False)
        query.add(Q(employees_assigned__returned_date__isnull=True), Q.AND)
        return self.filter(query).distinct()


class Hardware(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    hardware_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    serial_no = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(HardwareType, null=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(HardwareOwner, null=True, on_delete=models.SET_NULL)
    condition = models.ForeignKey(
        HardwareCondition, null=True, blank=True, on_delete=models.SET_NULL
    )
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    building = models.ForeignKey(Building, null=True, on_delete=models.SET_NULL)
    purchased_date = models.DateField(default=date.today)
    sold_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    objects = HardwareQuerySet.as_manager()

    def __str__(self) -> str:
        return self.hardware_id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.hardware_id:
            hardware_id = generate_unique_identifier(self.__class__.__name__, self.id)
            self.hardware_id = hardware_id
            return self.save()


class HardwareAssignmentManager(models.Manager):
    def create(self, **kwargs: Any) -> Any:
        """
        Ensure that any hardware being assigned to employee is first
        returned if previously assigned.
        """
        hardware = kwargs.get("hardware")
        employee = kwargs.get("employee")
        assignment_exists = HardwareAssignment.objects.filter(
            hardware=hardware, employee=employee, returned_date__isnull=True
        ).exists()
        if assignment_exists:
            raise ValidationError(
                "Hardware is already assigned to employee, please return existing assignment."
            )
        return super().create(**kwargs)


class HardwareAssignment(models.Model):
    assignment_id = models.CharField(max_length=10, null=True, blank=True)
    hardware = models.ForeignKey(
        Hardware,
        null=True,
        on_delete=models.SET_NULL,
        related_name="employees_assigned",
    )
    employee = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name="assigned_hardwares",
    )
    assignment_date = models.DateField(default=datetime.now)
    returned_date = models.DateField(null=True)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    objects = HardwareAssignmentManager()

    def __str__(self) -> str:
        return self.assignment_id

    @classmethod
    def from_db(
        cls, db: str | None, field_names: Collection[str], values: Collection[Any]
    ):
        """
        Store initialled loaded values from db. Use for comparing field values for update
        operations.
        """
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def check_unallowed_edit(self) -> None:
        """
        Disallow changing of Hardware or Employee for existing HardwareAssignment record. To
        change an employee's hardware, return existing assignment and create a new record.
        """
        if not self._state.adding and getattr(self, "_loaded_values", None):
            if (
                self.hardware.id != self._loaded_values["hardware_id"]
                or self.employee.emp_id != self._loaded_values["employee_id"]
            ):
                raise ValidationError(
                    "Editing Hardware Not Allowed, Please Create New Assignment"
                )

    def save(self, *args, **kwargs):
        self.check_unallowed_edit()
        super().save(*args, **kwargs)
        if not self.assignment_id:
            assignment_id = generate_unique_identifier(self.__class__.__name__, self.id)
            self.assignment_id = assignment_id
            self.save()


class LaptopOwner(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class LaptopScreenSize(models.Model):
    size_range = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.size_range


class LaptopManager(models.Manager):
    @transaction.atomic
    def create(self, hardware_data, laptop_data) -> Any:
        """
        Custom manager method that creates Laptop
        and related Hardware records

        Ensure only validated data (either via Forms
        or Serializers) is passed to this method.
        """
        hardware = Hardware.objects.create(**hardware_data)
        laptop = LaptopV2(hardware_id=hardware, **laptop_data)
        laptop.save()
        return laptop


class LaptopV2(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    hardware_id = models.OneToOneField(Hardware, on_delete=models.CASCADE)
    laptop_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    brand = models.ForeignKey(LaptopBrand, null=True, on_delete=models.SET_NULL)
    processor = models.CharField(max_length=255)
    ram_capacity = models.IntegerField(verbose_name="RAM (GB)")
    storage_capacity = models.IntegerField(verbose_name="Storage (GB)")
    screen_size = models.ForeignKey(
        LaptopScreenSize, null=True, on_delete=models.SET_NULL
    )
    is_touch = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    objects = LaptopManager()

    class Meta:
        verbose_name = "Laptop"
        verbose_name_plural = "Laptops"

    def __str__(self) -> str:
        return self.laptop_id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.laptop_id:
            laptop_id = generate_unique_identifier(self.__class__.__name__, self.id)
            self.laptop_id = laptop_id
            self.save(*args, **kwargs)


class MobileType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Mobile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    hardware_id = models.OneToOneField(Hardware, on_delete=models.CASCADE)
    mobile_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    brand = models.CharField(max_length=100)
    type = models.ForeignKey(MobileType, null=True, on_delete=models.SET_NULL)
    imei = models.CharField(max_length=15, unique=True)

    def __str__(self) -> str:
        return self.mobile_id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.mobile_id:
            mobile_id = generate_unique_identifier(self.__class__.__name__, self.id)
            self.mobile_id = mobile_id
            self.save(*args, **kwargs)
