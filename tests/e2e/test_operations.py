def test_idempotency_workflow(client):
    payload = {"amount": 100, "description": "Test operation"}

    first = client.post("/operations", headers={"Idempotency-Key": "abc123"}, json=payload)
    second = client.post("/operations", headers={"Idempotency-Key": "abc123"}, json=payload)
    conflict = client.post(
        "/operations",
        headers={"Idempotency-Key": "abc123"},
        json={"amount": 200, "description": "Different"},
    )

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json() == first.json()
    assert conflict.status_code == 409


def test_missing_key_and_invalid_payload(client):
    missing = client.post("/operations", json={"amount": 1, "description": "test"})
    invalid = client.post(
        "/operations",
        headers={"Idempotency-Key": "invalid"},
        json={"amount": 0, "description": "test"},
    )

    assert missing.status_code == 400
    assert invalid.status_code == 422


def test_idempotency_key_whitespace_is_normalized(client):
    payload = {"amount": 30, "description": "normalized key"}

    first = client.post("/operations", headers={"Idempotency-Key": " normalized "}, json=payload)
    second = client.post("/operations", headers={"Idempotency-Key": "normalized"}, json=payload)

    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json() == first.json()


def test_get_operation_and_health(client):
    created = client.post(
        "/operations",
        headers={"Idempotency-Key": "get-key"},
        json={"amount": 25, "description": "lookup"},
    )
    operation = client.get(f"/operations/{created.json()['id']}")

    assert client.get("/health").json() == {"status": "ok"}
    assert operation.status_code == 200
    assert operation.json() == created.json()
