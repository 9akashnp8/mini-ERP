import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from hardware.models import (
    HardwareType,
    HardwareOwner,
    HardwareCondition,
    Building,
    LaptopBrand,
    LaptopScreenSize,
    Hardware,
)
from employee.models import Employee, Location, Department, Designation


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture(scope="function")
def seed_hardware_owner():
    obj = HardwareOwner.objects.create(name="Test Hardware Owner")
    return obj.id


@pytest.fixture(scope="function")
def seed_hardware_type():
    obj = HardwareType.objects.create(name="Test Hardware Type")
    return obj.id


@pytest.fixture(scope="function")
def seed_hardware_condition():
    obj = HardwareCondition.objects.create(condition="Test Hardware Condition")
    return obj.id


@pytest.fixture(scope="function")
def seed_employee_location():
    obj = Location.objects.create(location="Test Location")
    return obj.location_id


@pytest.fixture(scope="function")
def seed_hardware_building():
    location = Location.objects.create(location="Test Location 2")
    obj = Building.objects.create(location=location, building="Test Building")
    return obj.id


@pytest.fixture(scope="function")
def seed_laptop_brand():
    obj = LaptopBrand.objects.create(brand_name="Test Laptop Brand")
    return obj.id


@pytest.fixture(scope="function")
def seed_laptop_screen_size():
    obj = LaptopScreenSize.objects.create(size_range='14" - 15"')
    return obj.id


@pytest.fixture(scope="function")
def seed_employee():
    user = User.objects.create(username="test_user", password="test_password")
    department = Department.objects.create(dept_name="test_department")
    designation = Designation.objects.create(
        dept_id=department, designation="test_designation"
    )
    branch = Location.objects.create(location="test_location")
    obj = Employee.objects.create(
        user=user,
        dept_id=department,
        desig_id=designation,
        emp_name="test_emp",
        emp_email="test_email",
        emp_phone="12345678",
        emp_status="Active",
        loc_id=branch,
    )
    return obj.emp_id


@pytest.fixture(scope="function")
def seed_hardware():
    hw_type = HardwareType.objects.create(name="test_hw_type")
    hw_owner = HardwareOwner.objects.create(name="test_hw_owner")
    hw_condition = HardwareCondition.objects.create(condition="test_hw_condition")
    hw_branch = Location.objects.create(location="test_hw_branch")
    hw_building = Building.objects.create(
        location=hw_branch, building="test_hw_building"
    )
    obj = Hardware.objects.create(
        serial_no="HW-001",
        type=hw_type,
        owner=hw_owner,
        condition=hw_condition,
        location=hw_branch,
        building=hw_building,
    )
    return obj.id
