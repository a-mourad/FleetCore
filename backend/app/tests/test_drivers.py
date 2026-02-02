def test_create_driver(client):
    org = client.post(
        "/api/v1/organisations",
        json={"name": "Org"},
    ).json()

    res = client.post(
        "/api/v1/drivers",
        json={
            "name": "ahmed",
            "organisation_id": org["id"],
        },
    )

    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "ahmed"
    assert data["organisation_id"] == org["id"]

def test_create_driver_organisation_must_exist(client):
    res = client.post(
        "/api/v1/drivers",
        json={
            "name": "John Doe",
            "organisation_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        },
    )

    assert res.status_code == 404
    assert "Organisation not found" in res.json()["detail"]


def test_list_drivers_by_organisation(client):
    org = client.post(
        "/api/v1/organisations",
        json={"name": "Org"},
    ).json()

    client.post(
        "/api/v1/drivers",
        json={"name": "ahmed", "organisation_id": org["id"]},
    )
    client.post(
        "/api/v1/drivers",
        json={"name": "mourad", "organisation_id": org["id"]},
    )

    res = client.get(f"/api/v1/drivers?organisation_id={org['id']}")

    assert res.status_code == 200
    assert len(res.json()) == 2
