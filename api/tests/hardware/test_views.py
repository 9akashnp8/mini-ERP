import logging
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_create_hardware_type(api_client) -> None:
    payload = {"name": "Test Hardware Type"}
    response = api_client.post("/api/hardware-type/", data=payload, format="json")
    hw_type_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]

    get_hw_type_response = api_client.get(
        f"/api/hardware-type/{hw_type_id}/", format="json"
    )
    assert get_hw_type_response.status_code == 200
    assert get_hw_type_response.data["name"] == payload["name"]


@pytest.mark.django_db
def test_update_hw_type(api_client) -> None:
    payload = {"name": "Test Hardware Type 2"}
    response = api_client.post("/api/hardware-type/", data=payload, format="json")
    hw_type_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]

    payload["name"] = "Updated Test Hardware Type"
    update_hw_type_response = api_client.patch(
        f"/api/hardware-type/{hw_type_id}/", data=payload, format="json"
    )
    assert update_hw_type_response.status_code == 200
    assert update_hw_type_response.data["name"] == payload["name"]

    update_404_response = api_client.patch(
        "/api/hardware-type/4/", data=payload, format="json"
    )
    assert update_404_response.status_code == 404


@pytest.mark.django_db
def test_delete_hardware_type(api_client) -> None:
    payload = {"name": "Test Hardware Type"}
    response = api_client.post("/api/hardware-type/", data=payload, format="json")
    hw_type_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]

    delete_response = api_client.delete(
        f"/api/hardware-type/{hw_type_id}/", format="json"
    )
    assert delete_response.status_code == 204

    delete_404_response = api_client.delete("/api/hardware-type/5/", format="json")
    assert delete_404_response.status_code == 404


@pytest.mark.django_db
def test_create_hardware_owner(api_client) -> None:
    payload = {"name": "Test Hardware Owner"}
    response = api_client.post("/api/hardware-owner/", data=payload, format="json")
    hw_owner_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]

    get_hw_owner_response = api_client.get(
        f"/api/hardware-owner/{hw_owner_id}/", format="json"
    )
    assert get_hw_owner_response.status_code == 200
    assert get_hw_owner_response.data["name"] == payload["name"]


@pytest.mark.django_db
def test_update_hardware_owner(api_client) -> None:
    payload = {"name": "Test Hardware Owner 2"}
    response = api_client.post("/api/hardware-owner/", data=payload, format="json")
    hw_owner_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]

    payload["name"] = "Updated Test Hardware Owner"
    update_hw_owner_response = api_client.patch(
        f"/api/hardware-owner/{hw_owner_id}/", data=payload, format="json"
    )
    assert update_hw_owner_response.status_code == 200
    assert update_hw_owner_response.data["name"] == payload["name"]

    update_404_response = api_client.patch(
        "/api/hardware-owner/4/", data=payload, format="json"
    )
    assert update_404_response.status_code == 404


@pytest.mark.django_db
def test_delete_hardware_owner(api_client) -> None:
    payload = {"name": "Test Hardware Owner"}
    response = api_client.post("/api/hardware-owner/", data=payload, format="json")
    hw_owner_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["name"] == payload["name"]

    delete_response = api_client.delete(
        f"/api/hardware-owner/{hw_owner_id}/", format="json"
    )
    assert delete_response.status_code == 204

    delete_404_response = api_client.delete("/api/hardware-owner/5/", format="json")
    assert delete_404_response.status_code == 404


@pytest.mark.django_db
def test_create_hardware_condition(api_client) -> None:
    payload = {"condition": "Test Hardware Condition"}
    response = api_client.post("/api/hardware-condition/", data=payload, format="json")
    hw_condition_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["condition"] == payload["condition"]

    get_hw_condition_response = api_client.get(
        f"/api/hardware-condition/{hw_condition_id}/", format="json"
    )
    assert get_hw_condition_response.status_code == 200
    assert get_hw_condition_response.data["condition"] == payload["condition"]


@pytest.mark.django_db
def test_update_hardware_condition(api_client) -> None:
    payload = {"condition": "Test Hardware Condition 2"}
    response = api_client.post("/api/hardware-condition/", data=payload, format="json")
    hw_condition_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["condition"] == payload["condition"]

    payload["condition"] = "Updated Test Hardware Owner"
    update_hw_condition_response = api_client.patch(
        f"/api/hardware-condition/{hw_condition_id}/", data=payload, format="json"
    )
    assert update_hw_condition_response.status_code == 200
    assert update_hw_condition_response.data["condition"] == payload["condition"]

    update_404_response = api_client.patch(
        "/api/hardware-condition/4/", data=payload, format="json"
    )
    assert update_404_response.status_code == 404


@pytest.mark.django_db
def test_delete_hardware_condition(api_client) -> None:
    payload = {"condition": "Test Hardware Condition"}
    response = api_client.post("/api/hardware-condition/", data=payload, format="json")
    hw_condition_id = response.data["id"]
    assert response.status_code == 201
    assert response.data["condition"] == payload["condition"]

    delete_response = api_client.delete(
        f"/api/hardware-condition/{hw_condition_id}/", format="json"
    )
    assert delete_response.status_code == 204

    delete_404_response = api_client.delete("/api/hardware-condition/5/", format="json")
    assert delete_404_response.status_code == 404


@pytest.mark.django_db
def test_create_hardware(
    api_client,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
) -> None:
    payload = {
        "serial_no": "SRL18",
        "type": seed_hardware_type,
        "owner": seed_hardware_owner,
        "condition": seed_hardware_condition,
        "location": seed_employee_location,
        "building": seed_hardware_building,
    }
    response = api_client.post("/api/hardware/", data=payload, format="json")
    hw_id = response.data["uuid"]
    assert response.status_code == 201
    assert response.data["serial_no"] == payload["serial_no"]

    get_hw_response = api_client.get(f"/api/hardware/{hw_id}/", format="json")
    assert get_hw_response.status_code == 200
    assert get_hw_response.data["serial_no"] == payload["serial_no"]


@pytest.mark.django_db
def test_update_hardware(
    api_client,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
) -> None:
    payload = {
        "serial_no": "SRL18",
        "type": seed_hardware_type,
        "owner": seed_hardware_owner,
        "condition": seed_hardware_condition,
        "location": seed_employee_location,
        "building": seed_hardware_building,
    }
    response = api_client.post("/api/hardware/", data=payload, format="json")
    hw_id = response.data["uuid"]
    assert response.status_code == 201
    assert response.data["serial_no"] == payload["serial_no"]

    payload["serial_no"] = "SRL180"
    update_hw_response = api_client.patch(
        f"/api/hardware/{hw_id}/", data=payload, format="json"
    )
    assert update_hw_response.status_code == 200
    assert update_hw_response.data["serial_no"] == payload["serial_no"]

    update_404_response = api_client.patch(
        "/api/hardware/4/", data=payload, format="json"
    )
    assert update_404_response.status_code == 404


@pytest.mark.django_db
def test_delete_hardware(
    api_client,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
) -> None:
    payload = {
        "serial_no": "SRL18",
        "type": seed_hardware_type,
        "owner": seed_hardware_owner,
        "condition": seed_hardware_condition,
        "location": seed_employee_location,
        "building": seed_hardware_building,
    }
    response = api_client.post("/api/hardware/", data=payload, format="json")
    hw_id = response.data["uuid"]
    assert response.status_code == 201
    assert response.data["serial_no"] == payload["serial_no"]

    delete_response = api_client.delete(f"/api/hardware/{hw_id}/", format="json")
    assert delete_response.status_code == 204

    delete_404_response = api_client.delete("/api/hardware/5/", format="json")
    assert delete_404_response.status_code == 404


@pytest.mark.django_db
def test_create_laptop_v1(
    api_client,
    seed_laptop_brand,
    seed_laptop_screen_size,
) -> None:
    payload = {
        "hardware_id": "",
        "laptop_sr_no": "SR-001",
        "processor": "i3 13th Gen",
        "ram_capacity": 4,
        "storage_capacity": 5,
        "brand": seed_laptop_brand,
        "screen_size": seed_laptop_screen_size,
    }
    post_response = api_client.post(
        "/api/laptop/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    laptop_id = post_response.data["id"]
    assert post_response.status_code == 201
    assert post_response.data["laptop_sr_no"] == payload["laptop_sr_no"]

    get_response = api_client.get(f"/api/laptop/{laptop_id}/", format="json")
    assert get_response.status_code == 200
    assert get_response.data["laptop_sr_no"] == payload["laptop_sr_no"]


@pytest.mark.django_db
def test_update_laptop_v1(
    api_client,
    seed_laptop_brand,
    seed_laptop_screen_size,
) -> None:
    payload = {
        "hardware_id": "",
        "laptop_sr_no": "SR-001",
        "processor": "i3 13th Gen",
        "ram_capacity": 4,
        "storage_capacity": 5,
        "brand": seed_laptop_brand,
        "screen_size": seed_laptop_screen_size,
    }
    post_response = api_client.post(
        "/api/laptop/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    laptop_id = post_response.data["id"]
    assert post_response.status_code == 201
    assert post_response.data["laptop_sr_no"] == payload["laptop_sr_no"]

    patch_payload = {"laptop_sr_no": "SR-002"}
    patch_response = api_client.patch(
        f"/api/laptop/{laptop_id}/",
        data=patch_payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert patch_response.status_code == 200
    assert patch_response.data["laptop_sr_no"] == patch_payload["laptop_sr_no"]

    patch_404_response = api_client.patch(
        "/api/hardware/4/", data=payload, format="json"
    )
    assert patch_404_response.status_code == 404


@pytest.mark.django_db
def test_delete_laptop_v1(
    api_client,
    seed_laptop_brand,
    seed_laptop_screen_size,
) -> None:
    payload = {
        "hardware_id": "",
        "laptop_sr_no": "SR-001",
        "processor": "i3 13th Gen",
        "ram_capacity": 4,
        "storage_capacity": 5,
        "brand": seed_laptop_brand,
        "screen_size": seed_laptop_screen_size,
    }
    post_response = api_client.post(
        "/api/laptop/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    laptop_id = post_response.data["id"]
    assert post_response.status_code == 201
    assert post_response.data["laptop_sr_no"] == payload["laptop_sr_no"]

    delete_response = api_client.delete(
        f"/api/laptop/{laptop_id}/",
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert delete_response.status_code == 204

    delete_404_response = api_client.delete("/api/hardware/5/", format="json")
    assert delete_404_response.status_code == 404


@pytest.mark.django_db
def test_create_laptop_v2(
    api_client,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
    seed_laptop_brand,
    seed_laptop_screen_size,
) -> None:
    payload = {
        "hardware_id": {
            "serial_no": "SRL100",
            "type": seed_hardware_type,
            "owner": seed_hardware_owner,
            "condition": seed_hardware_condition,
            "location": seed_employee_location,
            "building": seed_hardware_building,
        },
        "processor": "i3 13th Gen",
        "ram_capacity": 4,
        "storage_capacity": 5,
        "brand": seed_laptop_brand,
        "screen_size": seed_laptop_screen_size,
    }
    post_response = api_client.post(
        "/api/laptop/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    laptop_uuid = post_response.data["uuid"]
    assert post_response.status_code == 201
    assert (
        post_response.data["hardware_id"]["serial_no"]
        == payload["hardware_id"]["serial_no"]
    )

    get_response = api_client.get(
        f"/api/laptop/{laptop_uuid}/",
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    assert get_response.status_code == 200
    assert (
        get_response.data["hardware_id"]["serial_no"]
        == payload["hardware_id"]["serial_no"]
    )


@pytest.mark.django_db
def test_update_laptop_v2(
    api_client,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
    seed_laptop_brand,
    seed_laptop_screen_size,
) -> None:
    payload = {
        "hardware_id": {
            "serial_no": "SRL100",
            "type": seed_hardware_type,
            "owner": seed_hardware_owner,
            "condition": seed_hardware_condition,
            "location": seed_employee_location,
            "building": seed_hardware_building,
        },
        "processor": "i3 13th Gen",
        "ram_capacity": 4,
        "storage_capacity": 5,
        "brand": seed_laptop_brand,
        "screen_size": seed_laptop_screen_size,
    }
    post_response = api_client.post(
        "/api/laptop/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    laptop_uuid = post_response.data["uuid"]
    assert post_response.status_code == 201
    assert (
        post_response.data["hardware_id"]["serial_no"]
        == payload["hardware_id"]["serial_no"]
    )

    patch_payload = {"processor": "i5 12th Gen"}
    patch_response = api_client.patch(
        f"/api/laptop/{laptop_uuid}/",
        data=patch_payload,
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    assert patch_response.status_code == 200
    assert patch_response.data["processor"] == patch_payload["processor"]

    get_response = api_client.get(
        f"/api/laptop/{laptop_uuid}/",
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    assert get_response.status_code == 200
    assert get_response.data["processor"] == patch_payload["processor"]

    patch_404_response = api_client.patch(
        "/api/laptop/asv8-x4asd-v6xz/", data=payload, format="json"
    )
    assert patch_404_response.status_code == 404


@pytest.mark.django_db
def test_delete_laptop_v2(
    api_client,
    seed_hardware_type,
    seed_hardware_owner,
    seed_hardware_condition,
    seed_employee_location,
    seed_hardware_building,
    seed_laptop_brand,
    seed_laptop_screen_size,
) -> None:
    payload = {
        "hardware_id": {
            "serial_no": "SRL100",
            "type": seed_hardware_type,
            "owner": seed_hardware_owner,
            "condition": seed_hardware_condition,
            "location": seed_employee_location,
            "building": seed_hardware_building,
        },
        "processor": "i3 13th Gen",
        "ram_capacity": 4,
        "storage_capacity": 5,
        "brand": seed_laptop_brand,
        "screen_size": seed_laptop_screen_size,
    }
    post_response = api_client.post(
        "/api/laptop/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    laptop_uuid = post_response.data["uuid"]
    assert post_response.status_code == 201
    assert (
        post_response.data["hardware_id"]["serial_no"]
        == payload["hardware_id"]["serial_no"]
    )

    delete_response = api_client.delete(
        f"/api/laptop/{laptop_uuid}/",
        format="json",
        HTTP_ACCEPT="application/json; version=2",
    )
    assert delete_response.status_code == 204

    delete_404_response = api_client.delete(
        "/api/hardware/axz1-asd3-34as/", format="json"
    )
    assert delete_404_response.status_code == 404


@pytest.mark.django_db
def test_create_hardware_assignment(api_client, seed_employee, seed_hardware) -> None:
    payload = {
        "hardware": seed_hardware,
        "employee": seed_employee,
        "assignment_date": "2023-12-12",
    }
    post_response = api_client.post(
        "/api/hardware-assignment/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assignment_id = post_response.data["id"]
    assert post_response.status_code == 201

    get_response = api_client.get(
        f"/api/hardware-assignment/{assignment_id}/",
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert get_response.status_code == 200
    assert get_response.data["hardware"] == payload["hardware"]
    assert get_response.data["employee"] == payload["employee"]


@pytest.mark.django_db
def test_return_hardware(api_client, seed_employee, seed_hardware) -> None:
    payload = {
        "hardware": seed_hardware,
        "employee": seed_employee,
        "assignment_date": "2023-12-12",
    }
    post_response = api_client.post(
        "/api/hardware-assignment/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assignment_id = post_response.data["id"]
    assert post_response.status_code == 201

    return_payload = {"returned_date": "2023-12-31"}
    return_response = api_client.patch(
        f"/api/hardware-assignment/{assignment_id}/",
        data=return_payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert return_response.status_code == 200
    assert return_response.data["returned_date"] == return_payload["returned_date"]

    get_response = api_client.get(
        f"/api/hardware-assignment/{assignment_id}/",
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert get_response.status_code == 200
    assert get_response.data["returned_date"] == return_payload["returned_date"]


@pytest.mark.django_db
def test_delete_hardware_assignment_not_allowed(
    api_client, seed_employee, seed_hardware
) -> None:
    payload = {
        "hardware": seed_hardware,
        "employee": seed_employee,
        "assignment_date": "2023-12-12",
    }
    post_response = api_client.post(
        "/api/hardware-assignment/",
        data=payload,
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assignment_id = post_response.data["id"]
    assert post_response.status_code == 201

    delete_response = api_client.delete(
        f"/api/hardware-assignment/{assignment_id}/",
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert delete_response.status_code == 405

    get_response = api_client.get(
        f"/api/hardware-assignment/{assignment_id}/",
        format="json",
        HTTP_ACCEPT="application/json; version=1",
    )
    assert get_response.status_code == 200
