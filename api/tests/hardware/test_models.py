import pytest

from django.core.exceptions import ValidationError
from hardware.models import HardwareAssignment, Hardware


@pytest.mark.django_db
def test_disallow_edit_of_hw_assignment(
    seed_employee,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
) -> None:
    hw_obj_1 = Hardware.objects.create(
        serial_no="HW-001",
        type_id=seed_hardware_type,
        owner_id=seed_hardware_owner,
        condition_id=seed_hardware_condition,
        location_id=seed_employee_location,
        building_id=seed_hardware_building,
    )
    hw_obj_2 = Hardware.objects.create(
        serial_no="HW-002",
        type_id=seed_hardware_type,
        owner_id=seed_hardware_owner,
        condition_id=seed_hardware_condition,
        location_id=seed_employee_location,
        building_id=seed_hardware_building,
    )
    hw_assignment = HardwareAssignment.objects.create(
        employee_id=seed_employee, hardware=hw_obj_1
    )

    hw_assignment = HardwareAssignment.objects.get(id=hw_assignment.id)
    hw_assignment.hardware_id = hw_obj_2.id

    with pytest.raises(ValidationError):
        hw_assignment.save()

    hw_assignment = HardwareAssignment.objects.get(id=hw_assignment.id)
    assert hw_assignment.hardware_id == hw_obj_1.id
