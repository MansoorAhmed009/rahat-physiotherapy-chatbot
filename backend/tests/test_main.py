from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_chat_empty_message():
    resp = client.post("/chat", json={"message": ""})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_chat_whitespace_message():
    resp = client.post("/chat", json={"message": "   "})
    assert resp.status_code == 400


def test_appointment_missing_fields():
    resp = client.post("/appointment", json={"name": "John"})
    assert resp.status_code == 400
    assert "required" in resp.json()["detail"].lower()


def test_appointment_all_fields():
    resp = client.post("/appointment", json={
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "555-0000",
        "date": "2026-07-15",
        "time": "10:00",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "John Doe" in data["message"]


def test_lead_missing_fields():
    resp = client.post("/lead", json={"name": "Jane"})
    assert resp.status_code == 400


def test_lead_all_fields():
    resp = client.post("/lead", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "555-0001",
        "interest": "teeth whitening pricing",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "Jane Doe" in data["message"]
