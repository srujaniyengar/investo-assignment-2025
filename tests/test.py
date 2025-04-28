import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.models import StockData
import pandas as pd

class TestInvestoAssignment(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up FastAPI test client
        cls.client = TestClient(app)
        cls.sample_data = {
            "datetime": "2025-04-26T10:30:00",
            "open": 170.5,
            "high": 171.2,
            "low": 169.8,
            "close": 170.9,
            "volume": 1200000
        }

    def test_post_data(self):
        # Test POST /data endpoint
        response = self.client.post("/data", json=self.sample_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Record added successfully", response.json()["message"])

    def test_get_data(self):
        # Test GET /data endpoint
        response = self.client.get("/data")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        self.assertGreaterEqual(len(response.json()["data"]), 1)

    def test_sma_calculation(self):
        # Test SMA calculation logic
        data = pd.DataFrame([
            {"datetime": "2025-04-26T10:30:00", "close": 170.9},
            {"datetime": "2025-04-26T11:30:00", "close": 171.5},
            {"datetime": "2025-04-26T12:30:00", "close": 172.0},
        ])
        short_window = 2
        long_window = 3

        from app.sma import sma_crossover_strategy
        result = sma_crossover_strategy(data, short_window, long_window)
        self.assertIn("short_sma", result.columns)
        self.assertIn("long_sma", result.columns)
        self.assertIn("signal", result.columns)

        # Check SMA values
        self.assertAlmostEqual(result["short_sma"].iloc[-1], (171.5 + 172.0) / 2, places=2)
        self.assertAlmostEqual(result["long_sma"].iloc[-1], (170.9 + 171.5 + 172.0) / 3, places=2)

if __name__ == "__main__":
    unittest.main()