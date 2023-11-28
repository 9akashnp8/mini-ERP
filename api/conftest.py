import pytest

from rest_framework.test import APIClient

from hardware.models import (
    HardwareType,
    HardwareOwner,
    HardwareCondition,
    Building,
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
