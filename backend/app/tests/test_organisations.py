def test_create_root_organisation(client):
    res = client.post("/api/v1/organisations", json={"name": "Org A"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Org A"
    assert data["parent_id"] is None


def test_create_sub_organisation(client):
    parent = client.post(
        "/api/v1/organisations",
        json={"name": "Parent Org"},
    ).json()

    res = client.post(
        "/api/v1/organisations",
        json={"name": "Child Org", "parent_id": parent["id"]},
    )

    assert res.status_code == 201
    assert res.json()["parent_id"] == parent["id"]


def test_sub_organisation_cannot_have_children(client):
    parent = client.post(
        "/api/v1/organisations",
        json={"name": "Parent"},
    ).json()

    child = client.post(
        "/api/v1/organisations",
        json={"name": "Child", "parent_id": parent["id"]},
    ).json()

    res = client.post(
        "/api/v1/organisations",
        json={"name": "Invalid", "parent_id": child["id"]},
    )

    assert res.status_code == 400
    assert "cannot have children" in res.json()["detail"]
