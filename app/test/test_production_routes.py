

def test_get_production_log_by_id(client):
    response = client.post(
        "/production/",
        json={
            "well_id": 1,
            "production_date": "2025-01-01",
            "oil_bbl": 100,
            "gas_mscf": 50,
            "water_bbl": 20
        }
    )

    log_id = response.json()["id"]

    res = client.get(f"/production/{log_id}")
    assert res.status_code == 200
    assert res.json()["oil_bbl"] == 100


def test_get_missing_log_returns_404(client):
    res = client.get("/production/999")
    assert res.status_code == 404
