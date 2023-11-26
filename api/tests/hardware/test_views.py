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
