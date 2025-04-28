from fastapi.testclient import TestClient
from main import app, engine, SQLModel, Ticker_data

client = TestClient(app)


def setup_module(module):
    SQLModel.metadata.create_all(engine)


def teardown_module(module):
    SQLModel.metadata.drop_all(engine)


def test_create_data():
    payload = {
        "datetime": "2025-04-28T00:00:00",
        "open": 100.5,
        "high": 101.2,
        "low": 99.8,
        "close": 100.0,
        "volume": 1500,
        "instrument": "STOCK_A"
    }
    response = client.post("/data", json=payload)
    assert response.status_code == 200
    assert response.json() == payload


def test_read_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_calculate_performance():
    response = client.get("/strategy/performance")
    if response.status_code == 400:  # Insufficient data
        assert response.json()["detail"] == "Insufficient data for performance calculation"
    else:
        assert response.status_code == 200
        assert "total_return" in response.json()