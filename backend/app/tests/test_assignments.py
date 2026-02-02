from datetime import date


def setup_entities(client):
    org = client.post("/api/v1/organisations", json={"name": "Org"}).json()

    driver = client.post(
        "/api/v1/drivers",
        json={"name": "ahmed", "organisation_id": org["id"]},
    ).json()

    vehicule = client.post(
        "/api/v1/vehicules",
        json={
            "name": "Tesla",
            "plate_number": "SPM-123",
            "organisation_id": org["id"],
        },
    ).json()

    return org, driver, vehicule


def test_assign_driver_to_vehicle(client):
    org, driver, vehicule = setup_entities(client)

    res = client.post(
        "/api/v1/assignments",
        json={
            "driver_id": driver["id"],
            "vehicule_id": vehicule["id"],
            "start_date": date.today().isoformat(),
        },
    )
   # print(res.json())
    assert res.status_code == 201
    assert res.json()["end_date"] is None


def test_vehicle_cannot_have_two_active_drivers(client):
    org , driver1, vehicule = setup_entities(client)

    driver2 = client.post(
        "/api/v1/drivers",
        json={"name": "mourad", "organisation_id": vehicule["organisation_id"]},
    ).json()

    client.post(
        "/api/v1/assignments",
        json={"driver_id": driver1["id"], "vehicule_id": vehicule["id"],"start_date": date.today().isoformat()},
    )

    res = client.post(
        "/api/v1/assignments",
        json={"driver_id": driver2["id"], "vehicule_id": vehicule["id"],"start_date": date.today().isoformat(),},
    )

    assert  res.status_code == 409


def test_driver_cannot_have_two_active_vehicles(client):
    org, driver, vehicule1 = setup_entities(client)

    vehicule2 = client.post(
        "/api/v1/vehicules",
        json={
            "name": "Toyota",
            "plate_number": "CAR-262",
            "organisation_id": vehicule1["organisation_id"],
        },
    ).json()

    client.post(
        "/api/v1/assignments",
        json={"driver_id": driver["id"], "vehicule_id": vehicule1["id"],"start_date": date.today().isoformat()},
    )

    res = client.post(
        "/api/v1/assignments",
        json={"driver_id": driver["id"], "vehicule_id": vehicule2["id"],"start_date": date.today().isoformat()},
    )

    assert  res.status_code == 409


def test_driver_and_vehicle_must_belong_to_same_organisation(client):
    org1 = client.post("/api/v1/organisations", json={"name": "Org 1"}).json()
    org2 = client.post("/api/v1/organisations", json={"name": "Org 2"}).json()

    driver = client.post(
        "/api/v1/drivers",
        json={"name": "John", "organisation_id": org1["id"]},
    ).json()

    vehicule = client.post(
        "/api/v1/vehicules",
        json={
            "name": "BMW",
            "plate_number": "ORG2-CAR",
            "organisation_id": org2["id"],
        },
    ).json()

    res = client.post(
        "/api/v1/assignments",
        json={
            "driver_id": driver["id"],
            "vehicule_id": vehicule["id"],
            "start_date": date.today().isoformat()
        },
    )

    assert res.status_code == 400
    assert "same organisation" in res.json()["detail"]
