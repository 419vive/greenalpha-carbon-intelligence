"""
GreenAlpha FastAPI Direct Endpoint Testing
Tests endpoints using direct HTTP requests to avoid version conflicts
"""
import requests
import time
import json
import asyncio
import subprocess
import threading
import signal
import os
from typing import Dict, List, Any

class EndpointTester:
    """Direct endpoint testing using HTTP requests"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = []
        self.start_time = time.time()
        self.server_process = None
    
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
    
    def start_server(self):
        """Start the FastAPI server in background"""
        print("🚀 Starting FastAPI server...")
        try:
            # Start server in background
            self.server_process = subprocess.Popen([
                "python", "-m", "uvicorn", "main:app", 
                "--host", "0.0.0.0", "--port", "8000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait for server to start
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=1)
                    if response.status_code == 200:
                        print(f"✅ Server started successfully (attempt {attempt + 1})")
                        return True
                except:
                    pass
                time.sleep(1)
            
            print("❌ Server failed to start within 30 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the FastAPI server"""
        if self.server_process:
            print("🛑 Stopping FastAPI server...")
            self.server_process.terminate()
            self.server_process.wait()
            print("✅ Server stopped")
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        print("\n=== Testing Health Check Endpoint ===")
        
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Health check passed")
                print(f"   Status: {data.get('status', 'unknown')}")
                if 'components' in data:
                    components = data['components']
                    if 'data_manager' in components:
                        dm = components['data_manager']
                        print(f"   Countries loaded: {dm.get('countries_loaded', 0)}")
                        print(f"   Data records: {dm.get('data_records', 0)}")
                print(f"   Response time: {response_time:.2f}ms")
                
                self.add_result("health_check", "PASS", response_time, data)
                return True
            else:
                print(f"❌ Health check failed with status: {response.status_code}")
                self.add_result("health_check", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ Health check failed: {str(e)}")
            self.add_result("health_check", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_root_endpoint(self):
        """Test the root endpoint"""
        print("\n=== Testing Root Endpoint ===")
        
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Root endpoint passed")
                print(f"   Message: {data.get('message', 'N/A')}")
                print(f"   Version: {data.get('version', 'N/A')}")
                print(f"   Features: {len(data.get('features', []))} items")
                print(f"   Response time: {response_time:.2f}ms")
                
                self.add_result("root_endpoint", "PASS", response_time, data)
                return True
            else:
                print(f"❌ Root endpoint failed with status: {response.status_code}")
                self.add_result("root_endpoint", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ Root endpoint failed: {str(e)}")
            self.add_result("root_endpoint", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_carbon_calculate_smartphone(self):
        """Test carbon calculation for smartphone"""
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
        try:
            response = requests.post(f"{self.base_url}/carbon/calculate", 
                                   json=payload, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Smartphone calculation passed")
                print(f"   Total emissions: {data.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
                print(f"   Production: {data.get('production_emissions', 0):.2f} kg CO2e")
                print(f"   Transport: {data.get('transportation_emissions', 0):.2f} kg CO2e")
                print(f"   Carbon cost: ${data.get('carbon_cost_usd', 0):.2f}")
                print(f"   Confidence: {data.get('calculation_confidence', 0):.1f}%")
                print(f"   Response time: {response_time:.2f}ms")
                
                self.add_result("smartphone_calculation", "PASS", response_time, data)
                return True
            else:
                print(f"❌ Smartphone calculation failed with status: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                except:
                    print(f"   Error: {response.text}")
                self.add_result("smartphone_calculation", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ Smartphone calculation failed: {str(e)}")
            self.add_result("smartphone_calculation", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_carbon_calculate_laptop(self):
        """Test carbon calculation for laptop"""
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
        try:
            response = requests.post(f"{self.base_url}/carbon/calculate", 
                                   json=payload, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Laptop calculation passed")
                print(f"   Total emissions: {data.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
                print(f"   Production: {data.get('production_emissions', 0):.2f} kg CO2e")
                print(f"   Transport: {data.get('transportation_emissions', 0):.2f} kg CO2e")
                print(f"   Response time: {response_time:.2f}ms")
                
                self.add_result("laptop_calculation", "PASS", response_time, data)
                return True
            else:
                print(f"❌ Laptop calculation failed with status: {response.status_code}")
                self.add_result("laptop_calculation", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ Laptop calculation failed: {str(e)}")
            self.add_result("laptop_calculation", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_carbon_calculate_tshirt(self):
        """Test carbon calculation for T-shirt"""
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
        try:
            response = requests.post(f"{self.base_url}/carbon/calculate", 
                                   json=payload, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ T-shirt calculation passed")
                print(f"   Total emissions: {data.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
                print(f"   Production: {data.get('production_emissions', 0):.2f} kg CO2e")
                print(f"   Transport: {data.get('transportation_emissions', 0):.2f} kg CO2e")
                print(f"   Response time: {response_time:.2f}ms")
                
                self.add_result("tshirt_calculation", "PASS", response_time, data)
                return True
            else:
                print(f"❌ T-shirt calculation failed with status: {response.status_code}")
                self.add_result("tshirt_calculation", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ T-shirt calculation failed: {str(e)}")
            self.add_result("tshirt_calculation", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_batch_calculation(self):
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
        try:
            response = requests.post(f"{self.base_url}/carbon/calculate/batch", 
                                   json=batch_payload, timeout=15)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Batch calculation passed")
                print(f"   Total calculations: {data.get('total_calculations', 0)}")
                print(f"   Successful: {data.get('successful_calculations', 0)}")
                print(f"   Failed: {data.get('failed_calculations', 0)}")
                print(f"   Response time: {response_time:.2f}ms")
                
                if data.get("summary"):
                    summary = data["summary"]
                    print(f"   Total batch emissions: {summary.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
                    print(f"   Average emissions: {summary.get('average_emissions_kg_co2e', 0):.2f} kg CO2e")
                
                self.add_result("batch_calculation", "PASS", response_time, data)
                return True
            else:
                print(f"❌ Batch calculation failed with status: {response.status_code}")
                self.add_result("batch_calculation", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ Batch calculation failed: {str(e)}")
            self.add_result("batch_calculation", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_global_statistics(self):
        """Test global statistics endpoint"""
        print("\n=== Testing Global Statistics ===")
        
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/carbon/stats/global", timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Global statistics passed")
                print(f"   Response time: {response_time:.2f}ms")
                print(f"   Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                self.add_result("global_statistics", "PASS", response_time, data)
                return True
            else:
                print(f"❌ Global statistics failed with status: {response.status_code}")
                self.add_result("global_statistics", "FAIL", response_time, 
                              {"status_code": response.status_code})
                return False
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            print(f"❌ Global statistics failed: {str(e)}")
            self.add_result("global_statistics", "FAIL", response_time, {"error": str(e)})
            return False
    
    def test_performance_requirements(self):
        """Test performance requirements"""
        print("\n=== Testing Performance Requirements ===")
        
        payload = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight",
            "weight_kg": 0.2
        }
        
        response_times = []
        
        # Run 10 calculations
        for i in range(10):
            start_time = time.time()
            try:
                response = requests.post(f"{self.base_url}/carbon/calculate", 
                                       json=payload, timeout=10)
                response_time = (time.time() - start_time) * 1000
                response_times.append(response_time)
                
                if response.status_code != 200:
                    print(f"   Request {i+1} failed with status: {response.status_code}")
            except Exception as e:
                print(f"   Request {i+1} failed: {str(e)}")
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
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
            
            self.add_result("performance_test", "PASS" if performance_met else "FAIL", 
                          avg_response_time, performance_data)
            return performance_met
        else:
            print("❌ No successful responses for performance test")
            self.add_result("performance_test", "FAIL", 0, {"error": "No successful responses"})
            return False
    
    def get_summary(self):
        """Get test summary"""
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
    
    def run_all_tests(self):
        """Run all endpoint tests"""
        print("🚀 Starting GreenAlpha FastAPI Comprehensive Endpoint Testing")
        print("=" * 70)
        
        # Start server
        if not self.start_server():
            print("❌ Cannot start server, aborting tests")
            return
        
        try:
            test_functions = [
                self.test_health_endpoint,
                self.test_root_endpoint,
                self.test_carbon_calculate_smartphone,
                self.test_carbon_calculate_laptop,
                self.test_carbon_calculate_tshirt,
                self.test_batch_calculation,
                self.test_global_statistics,
                self.test_performance_requirements,
            ]
            
            passed_tests = 0
            
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
            
            summary = self.get_summary()
            
            print(f"Total Tests: {summary['total_tests']}")
            print(f"Passed: {summary['passed_tests']}")
            print(f"Failed: {summary['failed_tests']}")
            print(f"Success Rate: {summary['success_rate']:.1f}%")
            print(f"Average Response Time: {summary['average_response_time_ms']:.2f}ms")
            print(f"Total Test Duration: {summary['total_test_time_s']:.2f}s")
            
            # Performance analysis
            performance_results = [r for r in self.results if "calculation" in r["test_name"]]
            if performance_results:
                calc_times = [r["response_time_ms"] for r in performance_results]
                avg_calc_time = sum(calc_times) / len(calc_times)
                print(f"Average Calculation Time: {avg_calc_time:.2f}ms")
                print(f"Performance Target (<500ms): {'✅ MET' if avg_calc_time < 500 else '❌ NOT MET'}")
            
            # Detailed results
            print(f"\n📊 DETAILED TEST RESULTS:")
            print("-" * 50)
            for result in self.results:
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
            
        finally:
            self.stop_server()

if __name__ == "__main__":
    tester = EndpointTester()
    summary = tester.run_all_tests()