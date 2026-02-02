def test_create_vehicule(client):
    org = client.post(
        "/api/v1/organisations",
        json={"name": "Org"},
    ).json()

    res = client.post(
        "/api/v1/vehicules",
        json={
            "name": "Tesla",
            "plate_number": "ABC-123",
            "organisation_id": org["id"],
        },
    )

    assert res.status_code == 201
    assert res.json()["plate_number"] == "ABC-123"


def test_vehicle_plate_number_unique(client):
    org = client.post(
        "/api/v1/organisations",
        json={"name": "Org"},
    ).json()

    payload = {
        "name": "Tesla",
        "plate_number": "VEO-001",
        "organisation_id": org["id"],
    }

    client.post("/api/v1/vehicules", json=payload)
    res = client.post("/api/v1/vehicules", json=payload)

    assert res.status_code == 409
