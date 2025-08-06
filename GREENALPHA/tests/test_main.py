"""
Tests for main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "GreenAlpha Carbon Footprint Engine"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "GreenAlpha Carbon Footprint Engine" in data["message"]
    assert data["docs"] == "/docs"
    assert data["health"] == "/health"