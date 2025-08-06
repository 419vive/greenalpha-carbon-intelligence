"""
Tests for the Recommendation API Endpoints.

This test suite validates the functionality of the FastAPI recommendation routes.
"""
import unittest
import sys
import os
from fastapi.testclient import TestClient

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import app # Import the main FastAPI app

class TestRecommendationsAPI(unittest.TestCase):
    """
    Tests the core functionality of the recommendation API endpoints.
    """

    def setUp(self):
        """Set up the FastAPI test client for each test."""
        self.client = TestClient(app)

    def test_get_supplier_recommendations_success(self):
        """Test the POST /recommend/suppliers endpoint with a valid request."""
        request_body = {
            "weights": {
                "esg_score": 0.5,
                "cost_index": 0.5
            },
            "top_n": 3
        }
        response = self.client.post("/recommend/suppliers", json=request_body)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("items", data)
        self.assertIsInstance(data["items"], list)
        self.assertLessEqual(len(data["items"]), 3)

    def test_get_supplier_recommendations_pagination(self):
        """Test the pagination functionality of the /recommend/suppliers endpoint."""
        request_body = {
            "weights": {"esg_score": 1.0},
            "top_n": 5,
            "page": 2,
            "page_size": 2
        }
        response = self.client.post("/recommend/suppliers", json=request_body)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['page'], 2)
        self.assertEqual(len(data['items']), 2)
        # Assuming total of 6 suppliers in mock data
        self.assertEqual(data['total_suppliers'], 6) 
        self.assertEqual(data['total_pages'], 3)

    def test_get_alternatives_success(self):
        """Test the GET /recommend/alternatives/{supplier_id} endpoint."""
        response = self.client.get("/recommend/alternatives/S001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommended_suppliers", data)
        self.assertIsInstance(data["recommended_suppliers"], list)

    def test_get_alternatives_not_found(self):
        """Test the alternatives endpoint with an invalid supplier ID."""
        response = self.client.get("/recommend/alternatives/INVALID_ID")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_batch_recommendations_placeholder(self):
        """Test the POST /recommend/batch placeholder endpoint."""
        request_body = [
            {
                "weights": {"esg_score": 1.0},
                "top_n": 1
            }
        ]
        response = self.client.post("/recommend/batch", json=request_body)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

if __name__ == '__main__':
    unittest.main()
