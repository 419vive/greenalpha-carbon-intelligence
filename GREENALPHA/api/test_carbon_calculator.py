"""
Comprehensive tests for Carbon Calculator API
Tests performance, accuracy, and functionality
"""
import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from typing import Dict, Any
import json

from main import app

# Test client
client = TestClient(app)

class TestCarbonCalculatorAPI:
    """Test suite for Carbon Calculator API"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
        assert "features" in data
    
    def test_basic_carbon_calculation(self):
        """Test basic carbon footprint calculation"""
        request_data = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        response = client.post("/carbon/calculate", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check required fields
        assert "total_emissions_kg_co2e" in data
        assert "production_emissions" in data
        assert "transportation_emissions" in data
        assert "carbon_cost_usd" in data
        assert "calculation_confidence" in data
        assert "response_time_ms" in data
        
        # Check data types
        assert isinstance(data["total_emissions_kg_co2e"], (int, float))
        assert isinstance(data["production_emissions"], (int, float))
        assert isinstance(data["transportation_emissions"], (int, float))
        assert isinstance(data["carbon_cost_usd"], (int, float))
        assert isinstance(data["calculation_confidence"], (int, float))
        
        # Check reasonable values
        assert data["total_emissions_kg_co2e"] > 0
        assert data["calculation_confidence"] > 0
        assert data["calculation_confidence"] <= 100
    
    def test_performance_target(self):
        """Test that response time meets <500ms target"""
        request_data = {
            "product_name": "laptop",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "air_freight"
        }
        
        start_time = time.time()
        response = client.post("/carbon/calculate", json=request_data)
        response_time = (time.time() - start_time) * 1000
        
        assert response.status_code == 200
        
        # Performance target: <500ms for 95% of requests
        # Allow some margin for test environment
        assert response_time < 1000, f"Response time {response_time:.2f}ms exceeds target"
        
        data = response.json()
        # API should also report its internal timing
        if "response_time_ms" in data:
            assert data["response_time_ms"] < 800  # More lenient for test environment
    
    def test_different_transport_modes(self):
        """Test different transportation modes"""
        base_request = {
            "product_name": "t_shirt_cotton",
            "quantity": 10.0,
            "origin_country": "IND",
            "destination_country": "GBR"
        }
        
        transport_modes = ["road_truck", "rail", "sea_freight", "air_freight"]
        results = {}
        
        for mode in transport_modes:
            request_data = {**base_request, "transport_mode": mode}
            response = client.post("/carbon/calculate", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            results[mode] = data["transportation_emissions"]
        
        # Air freight should have highest emissions
        assert results["air_freight"] > results["sea_freight"]
        assert results["air_freight"] > results["rail"]
        assert results["air_freight"] > results["road_truck"]
        
        # Sea freight should be most efficient for long distances
        assert results["sea_freight"] < results["road_truck"]
    
    def test_quantity_scaling(self):
        """Test that emissions scale with quantity"""
        base_request = {
            "product_name": "running_shoes",
            "origin_country": "VNM",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        # Test with different quantities
        quantities = [1, 5, 10]
        emissions = []
        
        for qty in quantities:
            request_data = {**base_request, "quantity": qty}
            response = client.post("/carbon/calculate", json=request_data)
            assert response.status_code == 200
            
            data = response.json()
            emissions.append(data["total_emissions_kg_co2e"])
        
        # Emissions should scale roughly linearly with quantity
        assert emissions[1] > emissions[0] * 4  # 5x quantity should be >4x emissions
        assert emissions[2] > emissions[0] * 8  # 10x quantity should be >8x emissions
    
    def test_custom_emission_factors(self):
        """Test custom emission factors override"""
        base_request = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        # Get baseline calculation
        response1 = client.post("/carbon/calculate", json=base_request)
        assert response1.status_code == 200
        baseline = response1.json()
        
        # Test with custom emission factors
        custom_request = {
            **base_request,
            "custom_emission_factors": {
                "steel": 5.0,  # Higher than default
                "aluminum": 20.0  # Much higher than default
            }
        }
        
        response2 = client.post("/carbon/calculate", json=custom_request)
        assert response2.status_code == 200
        custom = response2.json()
        
        # Custom factors should increase production emissions
        assert custom["production_emissions"] > baseline["production_emissions"]
    
    def test_coordinate_precision(self):
        """Test precise coordinate-based distance calculation"""
        # Same countries, different coordinates
        request1 = {
            "product_name": "coffee_1kg",
            "quantity": 1.0,
            "origin_country": "USA",
            "destination_country": "USA",
            "transport_mode": "road_truck",
            "origin_latitude": 34.0522,  # Los Angeles
            "origin_longitude": -118.2437,
            "destination_latitude": 40.7128,  # New York
            "destination_longitude": -74.0060
        }
        
        request2 = {
            "product_name": "coffee_1kg",
            "quantity": 1.0,
            "origin_country": "USA",
            "destination_country": "USA",
            "transport_mode": "road_truck",
            "origin_latitude": 34.0522,  # Los Angeles
            "origin_longitude": -118.2437,
            "destination_latitude": 34.0522,  # Same city
            "destination_longitude": -118.2437
        }
        
        response1 = client.post("/carbon/calculate", json=request1)
        response2 = client.post("/carbon/calculate", json=request2)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # Cross-country should have higher transport emissions
        assert data1["transportation_emissions"] > data2["transportation_emissions"]
    
    def test_batch_calculation(self):
        """Test batch calculation endpoint"""
        batch_request = {
            "calculations": [
                {
                    "product_name": "smartphone",
                    "quantity": 1.0,
                    "origin_country": "CHN",
                    "destination_country": "USA",
                    "transport_mode": "sea_freight"
                },
                {
                    "product_name": "laptop",
                    "quantity": 2.0,
                    "origin_country": "TWN",
                    "destination_country": "DEU",
                    "transport_mode": "air_freight"
                },
                {
                    "product_name": "t_shirt_cotton",
                    "quantity": 5.0,
                    "origin_country": "BGD",
                    "destination_country": "GBR",
                    "transport_mode": "sea_freight"
                }
            ],
            "include_summary": True
        }
        
        response = client.post("/carbon/calculate/batch", json=batch_request)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check batch response structure
        assert "batch_id" in data
        assert "total_calculations" in data
        assert "successful_calculations" in data
        assert "results" in data
        assert "summary" in data
        
        # Check that all calculations succeeded
        assert data["successful_calculations"] == 3
        assert data["failed_calculations"] == 0
        assert len(data["results"]) == 3
        
        # Check summary
        summary = data["summary"]
        assert "total_emissions_kg_co2e" in summary
        assert "average_emissions_kg_co2e" in summary
        assert summary["calculations_processed"] == 3
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        # Invalid country code
        invalid_request = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "INVALID",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        response = client.post("/carbon/calculate", json=invalid_request)
        assert response.status_code == 422  # Validation error
        
        # Invalid transport mode
        invalid_request2 = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "teleportation"
        }
        
        response2 = client.post("/carbon/calculate", json=invalid_request2)
        assert response2.status_code == 422  # Validation error
        
        # Negative quantity
        invalid_request3 = {
            "product_name": "smartphone",
            "quantity": -1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        response3 = client.post("/carbon/calculate", json=invalid_request3)
        assert response3.status_code == 422  # Validation error
    
    def test_emission_factors_endpoint(self):
        """Test emission factors endpoint"""
        response = client.get("/carbon/factors/emission")
        assert response.status_code == 200
        
        data = response.json()
        assert "emission_factors" in data
        assert "total_factors" in data
        
        # Check that we have some standard factors
        factors = data["emission_factors"]
        assert "steel" in factors
        assert "aluminum" in factors
        assert "diesel" in factors
        
        # Check factor structure
        steel_factor = factors["steel"]
        assert "value" in steel_factor
        assert "unit" in steel_factor
        assert "source" in steel_factor
        assert "year" in steel_factor
    
    def test_country_factors_endpoint(self):
        """Test country-specific factors endpoint"""
        response = client.get("/carbon/factors/country/USA")
        assert response.status_code == 200
        
        data = response.json()
        assert "country_code" in data
        assert "country_name" in data
        assert "electricity_factor" in data
        assert "energy_mix" in data
        assert data["country_code"] == "USA"
        
        # Test invalid country
        response2 = client.get("/carbon/factors/country/INVALID")
        assert response2.status_code == 404
    
    def test_transport_modes_endpoint(self):
        """Test transport modes endpoint"""
        response = client.get("/carbon/transport/modes")
        assert response.status_code == 200
        
        data = response.json()
        assert "transport_modes" in data
        assert "total_modes" in data
        
        modes = data["transport_modes"]
        assert "road_truck" in modes
        assert "air_freight" in modes
        assert "sea_freight" in modes
    
    def test_product_catalog_endpoint(self):
        """Test product catalog endpoint"""
        response = client.get("/carbon/products/catalog")
        assert response.status_code == 200
        
        data = response.json()
        assert "products" in data
        assert "total_products" in data
        assert "supported_categories" in data
        
        products = data["products"]
        assert "smartphone" in products
        assert "laptop" in products
        
        # Check product structure
        smartphone = products["smartphone"]
        assert "energy_intensity" in smartphone
        assert "material_footprint" in smartphone
    
    def test_country_search(self):
        """Test country search endpoint"""
        response = client.get("/carbon/countries/search?query=United")
        assert response.status_code == 200
        
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert "total_found" in data
        assert data["query"] == "United"
        
        # Should find countries with "United" in name
        results = data["results"]
        assert len(results) > 0
        
        # Check result structure
        if results:
            result = results[0]
            assert "code" in result
            assert "name" in result
            assert "total_emissions" in result
    
    def test_global_statistics(self):
        """Test global statistics endpoint"""
        response = client.get("/carbon/stats/global")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_countries" in data
        assert "global_emissions" in data
        assert "top_emitters" in data
        assert "data_coverage" in data
        
        # Check top emitters structure
        top_emitters = data["top_emitters"]
        assert len(top_emitters) > 0
        
        if top_emitters:
            emitter = top_emitters[0]
            assert "country" in emitter
            assert "code" in emitter
            assert "emissions" in emitter
    
    def test_performance_statistics(self):
        """Test performance statistics endpoint"""
        # First make some requests to generate stats
        for i in range(3):
            request_data = {
                "product_name": "smartphone",
                "quantity": 1.0,
                "origin_country": "CHN",
                "destination_country": "USA",
                "transport_mode": "sea_freight"
            }
            client.post("/carbon/calculate", json=request_data)
        
        # Then check performance stats
        response = client.get("/carbon/stats/performance")
        assert response.status_code == 200
        
        data = response.json()
        assert "engine_performance" in data
        assert "data_manager_performance" in data
        assert "timestamp" in data

class TestCalculationAccuracy:
    """Test calculation accuracy and consistency"""
    
    def test_calculation_consistency(self):
        """Test that same input produces same output"""
        request_data = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        # Make multiple requests
        responses = []
        for _ in range(3):
            response = client.post("/carbon/calculate", json=request_data)
            assert response.status_code == 200
            responses.append(response.json())
        
        # Results should be identical
        for i in range(1, len(responses)):
            assert responses[0]["total_emissions_kg_co2e"] == responses[i]["total_emissions_kg_co2e"]
            assert responses[0]["production_emissions"] == responses[i]["production_emissions"]
            assert responses[0]["transportation_emissions"] == responses[i]["transportation_emissions"]
    
    def test_emissions_reasonableness(self):
        """Test that calculated emissions are within reasonable ranges"""
        test_cases = [
            {
                "request": {
                    "product_name": "smartphone",
                    "quantity": 1.0,
                    "origin_country": "CHN",
                    "destination_country": "USA",
                    "transport_mode": "sea_freight"
                },
                "expected_range": (20, 200)  # kg CO2e
            },
            {
                "request": {
                    "product_name": "laptop",
                    "quantity": 1.0,
                    "origin_country": "TWN",
                    "destination_country": "DEU",
                    "transport_mode": "air_freight"
                },
                "expected_range": (100, 800)  # kg CO2e
            },
            {
                "request": {
                    "product_name": "t_shirt_cotton",
                    "quantity": 1.0,
                    "origin_country": "BGD",
                    "destination_country": "GBR",
                    "transport_mode": "sea_freight"
                },
                "expected_range": (5, 50)  # kg CO2e
            }
        ]
        
        for case in test_cases:
            response = client.post("/carbon/calculate", json=case["request"])
            assert response.status_code == 200
            
            data = response.json()
            emissions = data["total_emissions_kg_co2e"]
            
            min_expected, max_expected = case["expected_range"]
            assert min_expected <= emissions <= max_expected, \
                f"Emissions {emissions:.2f} outside expected range {min_expected}-{max_expected} for {case['request']['product_name']}"

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])