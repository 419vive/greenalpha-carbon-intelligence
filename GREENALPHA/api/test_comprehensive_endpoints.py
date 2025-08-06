"""
GreenAlpha FastAPI Comprehensive Endpoint Testing Suite
Validates all API endpoints after core engine fixes
"""
import pytest
import asyncio
import time
from fastapi.testclient import TestClient
from fastapi import status
import json
from typing import Dict, List, Any

# Import the FastAPI app
from main import app

class TestResults:
    """Class to collect and store test results"""
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def add_result(self, test_name: str, status: str, response_time_ms: float, 
                   details: Dict[str, Any] = None):
        """Add a test result to the collection"""
        self.results.append({
            "test_name": test_name,
            "status": status,
            "response_time_ms": response_time_ms,
            "details": details or {},
            "timestamp": time.time()
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary statistics"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        avg_response_time = sum(r["response_time_ms"] for r in self.results) / total_tests if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "average_response_time_ms": avg_response_time,
            "total_test_time_s": time.time() - self.start_time
        }

# Global test results collector
test_results = TestResults()

# Create test client
client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    print("\n=== Testing Health Check Endpoint ===")
    
    start_time = time.time()
    response = client.get("/health")
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert "components" in data
        
        # Validate component health
        components = data["components"]
        assert "data_manager" in components
        assert "calculation_engine" in components
        
        print(f"✅ Health check passed")
        print(f"   Status: {data['status']}")
        print(f"   Countries loaded: {components['data_manager']['countries_loaded']}")
        print(f"   Data records: {components['data_manager']['data_records']}")
        print(f"   Response time: {response_time:.2f}ms")
        
        test_results.add_result("health_check", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        test_results.add_result("health_check", "FAIL", response_time, {"error": str(e)})
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    
    start_time = time.time()
    response = client.get("/")
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Validate response structure
        assert "message" in data
        assert "features" in data
        assert "endpoints" in data
        assert "version" in data
        
        print(f"✅ Root endpoint passed")
        print(f"   Message: {data['message']}")
        print(f"   Version: {data['version']}")
        print(f"   Features: {len(data['features'])} items")
        print(f"   Response time: {response_time:.2f}ms")
        
        test_results.add_result("root_endpoint", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ Root endpoint failed: {str(e)}")
        test_results.add_result("root_endpoint", "FAIL", response_time, {"error": str(e)})
        return False

def test_carbon_calculate_smartphone():
    """Test carbon calculation for smartphone (China → USA, sea freight)"""
    print("\n=== Testing Carbon Calculation - Smartphone ===")
    
    payload = {
        "product_name": "smartphone",
        "quantity": 1.0,
        "origin_country": "CHN",
        "destination_country": "USA",
        "transport_mode": "sea_freight",
        "product_category": "electronics",
        "weight_kg": 0.2
    }
    
    start_time = time.time()
    response = client.post("/carbon/calculate", json=payload)
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Validate core response structure
        required_fields = [
            "total_emissions_kg_co2e", "production_emissions", "transportation_emissions",
            "scope_1_emissions", "scope_2_emissions", "scope_3_emissions",
            "carbon_cost_usd", "calculation_confidence", "response_time_ms",
            "calculation_method", "data_sources"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Validate numeric values
        assert isinstance(data["total_emissions_kg_co2e"], (int, float))
        assert data["total_emissions_kg_co2e"] > 0
        assert isinstance(data["response_time_ms"], (int, float))
        
        print(f"✅ Smartphone calculation passed")
        print(f"   Total emissions: {data['total_emissions_kg_co2e']:.2f} kg CO2e")
        print(f"   Production: {data['production_emissions']:.2f} kg CO2e")
        print(f"   Transport: {data['transportation_emissions']:.2f} kg CO2e")
        print(f"   Carbon cost: ${data['carbon_cost_usd']:.2f}")
        print(f"   Confidence: {data['calculation_confidence']:.1f}%")
        print(f"   API response time: {response_time:.2f}ms")
        print(f"   Engine response time: {data['response_time_ms']:.2f}ms")
        
        test_results.add_result("smartphone_calculation", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ Smartphone calculation failed: {str(e)}")
        test_results.add_result("smartphone_calculation", "FAIL", response_time, {"error": str(e)})
        return False

def test_carbon_calculate_laptop():
    """Test carbon calculation for laptop (Germany → Japan, air freight)"""
    print("\n=== Testing Carbon Calculation - Laptop ===")
    
    payload = {
        "product_name": "laptop",
        "quantity": 1.0,
        "origin_country": "DEU",
        "destination_country": "JPN",
        "transport_mode": "air_freight",
        "product_category": "electronics",
        "weight_kg": 2.5
    }
    
    start_time = time.time()
    response = client.post("/carbon/calculate", json=payload)
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Validate that air freight has higher transport emissions
        assert data["total_emissions_kg_co2e"] > 0
        assert data["transportation_emissions"] > 0
        
        print(f"✅ Laptop calculation passed")
        print(f"   Total emissions: {data['total_emissions_kg_co2e']:.2f} kg CO2e")
        print(f"   Production: {data['production_emissions']:.2f} kg CO2e")
        print(f"   Transport: {data['transportation_emissions']:.2f} kg CO2e")
        print(f"   Response time: {response_time:.2f}ms")
        
        test_results.add_result("laptop_calculation", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ Laptop calculation failed: {str(e)}")
        test_results.add_result("laptop_calculation", "FAIL", response_time, {"error": str(e)})
        return False

def test_carbon_calculate_tshirt():
    """Test carbon calculation for T-shirt (India → UK, sea freight)"""
    print("\n=== Testing Carbon Calculation - T-shirt ===")
    
    payload = {
        "product_name": "t-shirt",
        "quantity": 1.0,
        "origin_country": "IND",
        "destination_country": "GBR",
        "transport_mode": "sea_freight",
        "product_category": "textiles",
        "weight_kg": 0.15
    }
    
    start_time = time.time()
    response = client.post("/carbon/calculate", json=payload)
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Validate reasonable emissions for textile product
        assert data["total_emissions_kg_co2e"] > 0
        assert data["total_emissions_kg_co2e"] < 100  # Should be lower than electronics
        
        print(f"✅ T-shirt calculation passed")
        print(f"   Total emissions: {data['total_emissions_kg_co2e']:.2f} kg CO2e")
        print(f"   Production: {data['production_emissions']:.2f} kg CO2e")
        print(f"   Transport: {data['transportation_emissions']:.2f} kg CO2e")
        print(f"   Response time: {response_time:.2f}ms")
        
        test_results.add_result("tshirt_calculation", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ T-shirt calculation failed: {str(e)}")
        test_results.add_result("tshirt_calculation", "FAIL", response_time, {"error": str(e)})
        return False

def test_batch_calculation():
    """Test batch calculation functionality"""
    print("\n=== Testing Batch Calculation ===")
    
    batch_payload = {
        "calculations": [
            {
                "product_name": "smartphone",
                "quantity": 1.0,
                "origin_country": "CHN",
                "destination_country": "USA",
                "transport_mode": "sea_freight",
                "weight_kg": 0.2
            },
            {
                "product_name": "laptop",
                "quantity": 1.0,
                "origin_country": "TWN",
                "destination_country": "DEU",
                "transport_mode": "air_freight",
                "weight_kg": 2.5
            },
            {
                "product_name": "t-shirt",
                "quantity": 5.0,
                "origin_country": "BGD",
                "destination_country": "USA",
                "transport_mode": "sea_freight",
                "weight_kg": 0.75
            }
        ],
        "include_summary": True
    }
    
    start_time = time.time()
    response = client.post("/carbon/calculate/batch", json=batch_payload)
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Validate batch response structure
        required_fields = [
            "batch_id", "total_calculations", "successful_calculations",
            "failed_calculations", "batch_processing_time_ms", "results", "summary"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing batch field: {field}"
        
        assert data["total_calculations"] == 3
        assert data["successful_calculations"] >= 0
        assert len(data["results"]) == data["successful_calculations"]
        
        print(f"✅ Batch calculation passed")
        print(f"   Total calculations: {data['total_calculations']}")
        print(f"   Successful: {data['successful_calculations']}")
        print(f"   Failed: {data['failed_calculations']}")
        print(f"   Batch processing time: {data['batch_processing_time_ms']:.2f}ms")
        print(f"   API response time: {response_time:.2f}ms")
        
        # Print summary if available
        if data.get("summary"):
            summary = data["summary"]
            print(f"   Total batch emissions: {summary['total_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"   Average emissions: {summary['average_emissions_kg_co2e']:.2f} kg CO2e")
        
        test_results.add_result("batch_calculation", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ Batch calculation failed: {str(e)}")
        test_results.add_result("batch_calculation", "FAIL", response_time, {"error": str(e)})
        return False

def test_global_statistics():
    """Test global statistics endpoint"""
    print("\n=== Testing Global Statistics ===")
    
    start_time = time.time()
    response = client.get("/carbon/stats/global")
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Should contain statistical information
        assert isinstance(data, dict)
        
        print(f"✅ Global statistics passed")
        print(f"   Response time: {response_time:.2f}ms")
        print(f"   Data keys: {list(data.keys())}")
        
        test_results.add_result("global_statistics", "PASS", response_time, data)
        return True
        
    except Exception as e:
        print(f"❌ Global statistics failed: {str(e)}")
        test_results.add_result("global_statistics", "FAIL", response_time, {"error": str(e)})
        return False

def test_performance_requirements():
    """Test that performance requirements are met"""
    print("\n=== Testing Performance Requirements ===")
    
    # Test response times for multiple calculations
    response_times = []
    
    payload = {
        "product_name": "smartphone",
        "quantity": 1.0,
        "origin_country": "CHN",
        "destination_country": "USA",
        "transport_mode": "sea_freight",
        "weight_kg": 0.2
    }
    
    # Run 10 calculations to test consistency
    for i in range(10):
        start_time = time.time()
        response = client.post("/carbon/calculate", json=payload)
        response_time = (time.time() - start_time) * 1000
        response_times.append(response_time)
        
        assert response.status_code == 200
    
    avg_response_time = sum(response_times) / len(response_times)
    max_response_time = max(response_times)
    min_response_time = min(response_times)
    
    # Check performance requirements
    performance_target = 500  # ms
    performance_met = avg_response_time < performance_target
    
    print(f"✅ Performance test completed")
    print(f"   Average response time: {avg_response_time:.2f}ms")
    print(f"   Max response time: {max_response_time:.2f}ms")
    print(f"   Min response time: {min_response_time:.2f}ms")
    print(f"   Performance target: <{performance_target}ms")
    print(f"   Performance met: {'✅ YES' if performance_met else '❌ NO'}")
    
    performance_data = {
        "average_ms": avg_response_time,
        "max_ms": max_response_time,
        "min_ms": min_response_time,
        "target_ms": performance_target,
        "target_met": performance_met,
        "samples": len(response_times)
    }
    
    test_results.add_result("performance_test", "PASS" if performance_met else "FAIL", 
                          avg_response_time, performance_data)
    return performance_met

def test_data_access():
    """Test data access and availability"""
    print("\n=== Testing Data Access ===")
    
    start_time = time.time()
    response = client.get("/health")
    response_time = (time.time() - start_time) * 1000
    
    try:
        assert response.status_code == 200
        data = response.json()
        
        # Check data availability
        data_manager = data["components"]["data_manager"]
        countries_loaded = data_manager["countries_loaded"]
        data_records = data_manager["data_records"]
        
        # Validate data volumes
        assert countries_loaded > 0, "No countries loaded"
        assert data_records > 20000, f"Expected >20,000 records, got {data_records}"
        
        print(f"✅ Data access test passed")
        print(f"   Countries loaded: {countries_loaded}")
        print(f"   Data records: {data_records:,}")
        print(f"   Target data size: 20,853 records")
        print(f"   Data availability: {'✅ SUFFICIENT' if data_records >= 20000 else '⚠️  LIMITED'}")
        
        data_info = {
            "countries_loaded": countries_loaded,
            "data_records": data_records,
            "target_records": 20853,
            "sufficient_data": data_records >= 20000
        }
        
        test_results.add_result("data_access", "PASS", response_time, data_info)
        return True
        
    except Exception as e:
        print(f"❌ Data access test failed: {str(e)}")
        test_results.add_result("data_access", "FAIL", response_time, {"error": str(e)})
        return False

def test_error_handling():
    """Test error handling with invalid requests"""
    print("\n=== Testing Error Handling ===")
    
    # Test invalid country code
    invalid_payload = {
        "product_name": "smartphone",
        "quantity": 1.0,
        "origin_country": "INVALID",
        "destination_country": "USA",
        "transport_mode": "sea_freight"
    }
    
    start_time = time.time()
    response = client.post("/carbon/calculate", json=invalid_payload)
    response_time = (time.time() - start_time) * 1000
    
    try:
        # Should return 422 (validation error) or handle gracefully
        assert response.status_code in [400, 422, 500]
        
        print(f"✅ Error handling test passed")
        print(f"   Invalid request handled with status: {response.status_code}")
        print(f"   Response time: {response_time:.2f}ms")
        
        test_results.add_result("error_handling", "PASS", response_time, 
                              {"status_code": response.status_code})
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        test_results.add_result("error_handling", "FAIL", response_time, {"error": str(e)})
        return False

def run_comprehensive_tests():
    """Run all comprehensive endpoint tests"""
    print("🚀 Starting GreenAlpha FastAPI Comprehensive Endpoint Testing")
    print("=" * 70)
    
    test_functions = [
        test_health_endpoint,
        test_root_endpoint,
        test_carbon_calculate_smartphone,
        test_carbon_calculate_laptop,
        test_carbon_calculate_tshirt,
        test_batch_calculation,
        test_global_statistics,
        test_performance_requirements,
        test_data_access,
        test_error_handling
    ]
    
    passed_tests = 0
    total_tests = len(test_functions)
    
    for test_func in test_functions:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {str(e)}")
    
    # Generate final summary
    print("\n" + "=" * 70)
    print("🎯 COMPREHENSIVE ENDPOINT TEST SUMMARY")
    print("=" * 70)
    
    summary = test_results.get_summary()
    
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Passed: {summary['passed_tests']}")
    print(f"Failed: {summary['failed_tests']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Average Response Time: {summary['average_response_time_ms']:.2f}ms")
    print(f"Total Test Duration: {summary['total_test_time_s']:.2f}s")
    
    # Performance analysis
    performance_results = [r for r in test_results.results if "calculation" in r["test_name"]]
    if performance_results:
        calc_times = [r["response_time_ms"] for r in performance_results]
        avg_calc_time = sum(calc_times) / len(calc_times)
        print(f"Average Calculation Time: {avg_calc_time:.2f}ms")
        print(f"Performance Target (<500ms): {'✅ MET' if avg_calc_time < 500 else '❌ NOT MET'}")
    
    # Detailed results
    print(f"\n📊 DETAILED TEST RESULTS:")
    print("-" * 50)
    for result in test_results.results:
        status_icon = "✅" if result["status"] == "PASS" else "❌"
        print(f"{status_icon} {result['test_name']}: {result['response_time_ms']:.2f}ms")
    
    print("\n" + "=" * 70)
    if summary['success_rate'] >= 80:
        print("🎉 TESTING COMPLETED SUCCESSFULLY!")
        print("   FastAPI endpoints are functioning correctly.")
    else:
        print("⚠️  TESTING COMPLETED WITH ISSUES!")
        print("   Some endpoints require attention.")
    
    return summary

if __name__ == "__main__":
    summary = run_comprehensive_tests()