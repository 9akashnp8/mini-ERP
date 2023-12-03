import pytest

from rest_framework.test import APIClient

from hardware.models import (
    HardwareType,
    HardwareOwner,
    HardwareCondition,
    Building,
    LaptopBrand,
    LaptopScreenSize,
)
from employee.models import Location


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
