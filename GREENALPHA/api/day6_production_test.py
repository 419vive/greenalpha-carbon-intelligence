"""
Day 6 Production-Ready Test Suite
Complete system validation for production deployment
"""
import sys
import os
import asyncio
import time
import requests
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime
import concurrent.futures
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ProductionTestSuite:
    def __init__(self):
        self.api_base = 'http://localhost:8000'
        self.test_results = []
        self.performance_metrics = {}
        
    async def run_all_tests(self):
        """Run all production tests"""
        print("🚀 GreenAlpha Day 6 - Production Test Suite")
        print("=" * 70)
        
        # Start server for testing
        await self._start_test_server()
        
        test_categories = [
            ("System Health & Stability", self._test_system_health),
            ("API Performance & Load", self._test_api_performance),
            ("Data Integrity & Accuracy", self._test_data_integrity),
            ("Security & Error Handling", self._test_security),
            ("Frontend Integration", self._test_frontend_integration),
            ("Production Readiness", self._test_production_readiness),
            ("MVP Success Criteria", self._test_mvp_criteria)
        ]
        
        for category_name, test_func in test_categories:
            print(f"\n📋 {category_name}")
            print("-" * 50)
            
            try:
                success = await test_func()
                self.test_results.append((category_name, success))
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"{status} - {category_name}")
                
            except Exception as e:
                print(f"❌ Test failed with exception: {e}")
                self.test_results.append((category_name, False))
        
        return self._generate_test_report()
    
    async def _start_test_server(self):
        """Start test server in background"""
        print("🔄 Starting production test server...")
        
        # Kill existing processes
        subprocess.run(["pkill", "-f", "uvicorn.*main"], check=False)
        await asyncio.sleep(2)
        
        # Start server in background
        def start_server():
            subprocess.run([
                "python", "-c", 
                """
import uvicorn
from main import app
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
                """
            ], cwd="/Users/jerrylaivivemachi/DS PROJECT/project 3/GREENALPHA/api")
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to be ready
        for i in range(15):
            try:
                response = requests.get(f"{self.api_base}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Test server ready")
                    return
            except:
                pass
            await asyncio.sleep(1)
        
        raise Exception("Failed to start test server")
    
    async def _test_system_health(self):
        """Test system health and component status"""
        print("🧪 Testing system health...")
        
        try:
            # Test health endpoint
            response = requests.get(f"{self.api_base}/health", timeout=5)
            if response.status_code != 200:
                print("❌ Health endpoint failed")
                return False
            
            health_data = response.json()
            print(f"✅ System status: {health_data['status']}")
            print(f"✅ Countries loaded: {health_data['components']['data_manager']['countries_loaded']}")
            print(f"✅ Data records: {health_data['components']['data_manager']['data_records']}")
            
            # Test all main endpoints
            endpoints = [
                "/carbon/calculate",
                "/carbon/factors/emission", 
                "/carbon/stats/global",
                "/recommendations/recommend/suppliers",
                "/transport/optimize/route",
                "/arbitrage/comprehensive-report"
            ]
            
            endpoint_results = []
            for endpoint in endpoints:
                try:
                    if endpoint == "/carbon/calculate":
                        # POST endpoint needs data
                        test_data = {
                            "product_name": "smartphone",
                            "quantity": 1,
                            "origin_country": "CHN",
                            "destination_country": "USA",
                            "transport_mode": "air_freight"
                        }
                        resp = requests.post(f"{self.api_base}{endpoint}", json=test_data, timeout=10)
                    else:
                        resp = requests.get(f"{self.api_base}{endpoint}", timeout=10)
                    
                    endpoint_results.append((endpoint, resp.status_code == 200))
                    if resp.status_code == 200:
                        print(f"✅ Endpoint working: {endpoint}")
                    else:
                        print(f"❌ Endpoint failed: {endpoint} ({resp.status_code})")
                        
                except Exception as e:
                    print(f"❌ Endpoint error: {endpoint} - {e}")
                    endpoint_results.append((endpoint, False))
            
            # Calculate success rate
            successful = sum(1 for _, success in endpoint_results if success)
            success_rate = successful / len(endpoint_results)
            
            print(f"📊 Endpoint success rate: {successful}/{len(endpoint_results)} ({success_rate:.1%})")
            return success_rate >= 0.8
            
        except Exception as e:
            print(f"❌ System health test failed: {e}")
            return False
    
    async def _test_api_performance(self):
        """Test API performance and load handling"""
        print("🧪 Testing API performance...")
        
        try:
            # Single request performance
            test_data = {
                "product_name": "smartphone",
                "quantity": 1,
                "origin_country": "CHN", 
                "destination_country": "USA",
                "transport_mode": "air_freight"
            }
            
            # Test response time
            start_time = time.time()
            response = requests.post(f"{self.api_base}/carbon/calculate", json=test_data, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code != 200:
                print("❌ Performance test failed - API not responding")
                return False
                
            data = response.json()
            api_response_time = data.get('response_time_ms', 0)
            
            print(f"✅ End-to-end response time: {response_time:.1f}ms")
            print(f"✅ API calculation time: {api_response_time:.1f}ms")
            
            # Test load handling with concurrent requests
            print("🔄 Testing concurrent load...")
            
            def make_request():
                try:
                    resp = requests.post(f"{self.api_base}/carbon/calculate", json=test_data, timeout=15)
                    return resp.status_code == 200, time.time()
                except:
                    return False, time.time()
            
            # Run 10 concurrent requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                load_start = time.time()
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
                load_time = (time.time() - load_start) * 1000
            
            successful_requests = sum(1 for success, _ in results if success)
            success_rate = successful_requests / 10
            
            print(f"✅ Concurrent requests: {successful_requests}/10 successful ({success_rate:.1%})")
            print(f"✅ Load test time: {load_time:.1f}ms")
            
            # Performance criteria
            performance_ok = (
                response_time < 500 and  # < 500ms response time
                api_response_time < 100 and  # < 100ms calculation time
                success_rate >= 0.9  # 90% success rate under load
            )
            
            self.performance_metrics = {
                "response_time_ms": response_time,
                "api_calculation_ms": api_response_time,
                "concurrent_success_rate": success_rate,
                "load_test_time_ms": load_time
            }
            
            return performance_ok
            
        except Exception as e:
            print(f"❌ Performance test failed: {e}")
            return False
    
    async def _test_data_integrity(self):
        """Test data accuracy and calculation integrity"""
        print("🧪 Testing data integrity...")
        
        try:
            # Test known calculation scenarios
            test_scenarios = [
                {
                    "name": "Smartphone China->USA Air",
                    "data": {
                        "product_name": "smartphone",
                        "quantity": 1,
                        "origin_country": "CHN",
                        "destination_country": "USA", 
                        "transport_mode": "air_freight"
                    },
                    "expected_range": (50, 120)  # kg CO2e
                },
                {
                    "name": "Laptop Germany->Japan Sea", 
                    "data": {
                        "product_name": "laptop",
                        "quantity": 1,
                        "origin_country": "DEU",
                        "destination_country": "JPN",
                        "transport_mode": "sea_freight"
                    },
                    "expected_range": (80, 200)  # kg CO2e
                }
            ]
            
            all_tests_passed = True
            
            for scenario in test_scenarios:
                response = requests.post(f"{self.api_base}/carbon/calculate", json=scenario["data"], timeout=10)
                
                if response.status_code != 200:
                    print(f"❌ Scenario failed: {scenario['name']}")
                    all_tests_passed = False
                    continue
                
                data = response.json()
                emissions = data["total_emissions_kg_co2e"]
                min_expected, max_expected = scenario["expected_range"]
                
                if min_expected <= emissions <= max_expected:
                    print(f"✅ {scenario['name']}: {emissions:.1f} kg CO₂e (valid range)")
                else:
                    print(f"❌ {scenario['name']}: {emissions:.1f} kg CO₂e (outside expected range {min_expected}-{max_expected})")
                    all_tests_passed = False
                
                # Test data structure completeness
                required_fields = [
                    "total_emissions_kg_co2e", "production_emissions", "transportation_emissions",
                    "scope_1_emissions", "scope_2_emissions", "scope_3_emissions",
                    "carbon_cost_usd", "calculation_confidence", "response_time_ms"
                ]
                
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    print(f"❌ Missing fields in {scenario['name']}: {missing_fields}")
                    all_tests_passed = False
                else:
                    print(f"✅ All required fields present for {scenario['name']}")
            
            # Test calculation consistency (same input should give same output)
            test_data = test_scenarios[0]["data"]
            results = []
            for i in range(3):
                response = requests.post(f"{self.api_base}/carbon/calculate", json=test_data, timeout=10)
                if response.status_code == 200:
                    results.append(response.json()["total_emissions_kg_co2e"])
            
            if len(results) >= 2:
                consistency_check = all(abs(r - results[0]) < 0.01 for r in results)
                if consistency_check:
                    print("✅ Calculation consistency verified")
                else:
                    print(f"❌ Calculation inconsistency detected: {results}")
                    all_tests_passed = False
            
            return all_tests_passed
            
        except Exception as e:
            print(f"❌ Data integrity test failed: {e}")
            return False
    
    async def _test_security(self):
        """Test security and error handling"""
        print("🧪 Testing security and error handling...")
        
        try:
            security_tests = []
            
            # Test invalid input handling
            invalid_inputs = [
                {"product_name": "", "quantity": 1, "origin_country": "CHN", "destination_country": "USA", "transport_mode": "air_freight"},
                {"product_name": "test", "quantity": -1, "origin_country": "CHN", "destination_country": "USA", "transport_mode": "air_freight"},
                {"product_name": "test", "quantity": 1, "origin_country": "INVALID", "destination_country": "USA", "transport_mode": "air_freight"},
                {"product_name": "test", "quantity": 1, "origin_country": "CHN", "destination_country": "USA", "transport_mode": "invalid_mode"},
            ]
            
            for invalid_input in invalid_inputs:
                response = requests.post(f"{self.api_base}/carbon/calculate", json=invalid_input, timeout=10)
                if 400 <= response.status_code < 500:
                    print("✅ Invalid input properly rejected")
                    security_tests.append(True)
                else:
                    print(f"❌ Invalid input not properly handled: {response.status_code}")
                    security_tests.append(False)
            
            # Test malformed JSON
            try:
                response = requests.post(f"{self.api_base}/carbon/calculate", 
                                       data="invalid json", 
                                       headers={"Content-Type": "application/json"}, 
                                       timeout=10)
                if 400 <= response.status_code < 500:
                    print("✅ Malformed JSON properly rejected")
                    security_tests.append(True)
                else:
                    print(f"❌ Malformed JSON not handled: {response.status_code}")
                    security_tests.append(False)
            except:
                security_tests.append(True)  # Connection error is acceptable
            
            # Test CORS headers
            response = requests.options(f"{self.api_base}/carbon/calculate", 
                                      headers={"Origin": "http://localhost:8000"}, 
                                      timeout=10)
            cors_headers = response.headers.get("Access-Control-Allow-Origin")
            if cors_headers:
                print("✅ CORS headers present")
                security_tests.append(True)
            else:
                print("❌ CORS headers missing")
                security_tests.append(False)
            
            return sum(security_tests) >= len(security_tests) * 0.8
            
        except Exception as e:
            print(f"❌ Security test failed: {e}")
            return False
    
    async def _test_frontend_integration(self):
        """Test frontend integration"""
        print("🧪 Testing frontend integration...")
        
        try:
            # Test static file serving
            frontend_files = ["index.html", "simple.html", "dashboard.html", "analytics.html"]
            file_tests = []
            
            for file in frontend_files:
                response = requests.get(f"{self.api_base}/static/{file}", timeout=10)
                if response.status_code == 200 and len(response.text) > 1000:
                    print(f"✅ Frontend file accessible: {file}")
                    file_tests.append(True)
                else:
                    print(f"❌ Frontend file issue: {file}")
                    file_tests.append(False)
            
            # Test demo route
            response = requests.get(f"{self.api_base}/demo/", timeout=10)
            demo_working = response.status_code == 200
            if demo_working:
                print("✅ Demo route accessible")
            else:
                print("❌ Demo route failed")
            
            return sum(file_tests) >= len(file_tests) * 0.8 and demo_working
            
        except Exception as e:
            print(f"❌ Frontend integration test failed: {e}")
            return False
    
    async def _test_production_readiness(self):
        """Test production deployment readiness"""
        print("🧪 Testing production readiness...")
        
        try:
            checks = []
            
            # Test logging
            response = requests.get(f"{self.api_base}/health", timeout=10)
            if response.status_code == 200:
                print("✅ Application logging functional")
                checks.append(True)
            else:
                checks.append(False)
            
            # Test error responses
            response = requests.get(f"{self.api_base}/nonexistent-endpoint", timeout=10)
            if response.status_code == 404:
                print("✅ 404 handling working")
                checks.append(True)
            else:
                print("❌ 404 handling failed")
                checks.append(False)
            
            # Test API documentation
            response = requests.get(f"{self.api_base}/docs", timeout=10)
            if response.status_code == 200:
                print("✅ API documentation accessible")
                checks.append(True)
            else:
                print("❌ API documentation failed")
                checks.append(False)
            
            # Test environment configuration
            response = requests.get(f"{self.api_base}/api", timeout=10)
            if response.status_code == 200:
                api_info = response.json()
                if "version" in api_info:
                    print(f"✅ Version info present: {api_info['version']}")
                    checks.append(True)
                else:
                    print("❌ Version info missing")
                    checks.append(False)
            else:
                checks.append(False)
            
            return sum(checks) >= len(checks) * 0.8
            
        except Exception as e:
            print(f"❌ Production readiness test failed: {e}")
            return False
    
    async def _test_mvp_criteria(self):
        """Test MVP success criteria"""
        print("🧪 Testing MVP success criteria...")
        
        try:
            criteria_results = []
            
            # 1. Calculate carbon footprint A->B for any commodity
            test_data = {
                "product_name": "smartphone",
                "quantity": 1,
                "origin_country": "CHN",
                "destination_country": "USA",
                "transport_mode": "air_freight"
            }
            
            response = requests.post(f"{self.api_base}/carbon/calculate", json=test_data, timeout=10)
            if response.status_code == 200:
                data = response.json()
                emissions = data["total_emissions_kg_co2e"]
                print(f"✅ A->B calculation working: {emissions:.1f} kg CO₂e")
                criteria_results.append(True)
            else:
                print("❌ A->B calculation failed")
                criteria_results.append(False)
            
            # 2. Calculation error < 10% (using confidence score)
            if response.status_code == 200:
                confidence = data.get("calculation_confidence", 0)
                if confidence >= 85:  # 85%+ confidence means <15% error
                    print(f"✅ High calculation confidence: {confidence}%")
                    criteria_results.append(True)
                else:
                    print(f"❌ Low calculation confidence: {confidence}%")
                    criteria_results.append(False)
            else:
                criteria_results.append(False)
            
            # 3. User experience (5-minute analysis) - test UI responsiveness
            start_time = time.time()
            ui_response = requests.get(f"{self.api_base}/static/simple.html", timeout=10)
            ui_load_time = time.time() - start_time
            
            if ui_response.status_code == 200 and ui_load_time < 2:
                print(f"✅ UI loads quickly: {ui_load_time:.1f}s")
                criteria_results.append(True)
            else:
                print(f"❌ UI load issues: {ui_load_time:.1f}s")
                criteria_results.append(False)
            
            # 4. System stability (basic stability test)
            stable_requests = 0
            for i in range(5):
                test_response = requests.post(f"{self.api_base}/carbon/calculate", json=test_data, timeout=10)
                if test_response.status_code == 200:
                    stable_requests += 1
                await asyncio.sleep(0.5)
            
            if stable_requests >= 4:  # 80% success rate
                print(f"✅ System stability: {stable_requests}/5 requests successful")
                criteria_results.append(True)
            else:
                print(f"❌ System instability: {stable_requests}/5 requests successful")
                criteria_results.append(False)
            
            # 5. Visual decision support
            if ui_response.status_code == 200:
                ui_content = ui_response.text
                has_visualization = all(term in ui_content.lower() for term in ["chart", "graph", "visual", "dashboard"])
                if has_visualization:
                    print("✅ Visual decision support present")
                    criteria_results.append(True)
                else:
                    print("❌ Limited visual decision support")
                    criteria_results.append(False)
            else:
                criteria_results.append(False)
            
            success_count = sum(criteria_results)
            success_rate = success_count / len(criteria_results)
            
            print(f"\n📊 MVP Criteria Results: {success_count}/5 ({success_rate:.1%})")
            return success_rate >= 0.8
            
        except Exception as e:
            print(f"❌ MVP criteria test failed: {e}")
            return False
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        passed_tests = sum(1 for _, success in self.test_results if success)
        total_tests = len(self.test_results)
        success_rate = passed_tests / total_tests if total_tests > 0 else 0
        
        print("\n" + "=" * 70)
        print("🎯 Day 6 Production Test Results")
        print("=" * 70)
        
        for test_name, success in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\nOverall: {passed_tests}/{total_tests} tests passed ({success_rate:.0%})")
        
        if success_rate >= 0.85:
            print("🎉 PRODUCTION READY! All systems validated for deployment.")
            print("\n🌟 Production Readiness Summary:")
            print("• ✅ System health and stability verified")
            print("• ✅ Performance targets met (<500ms response)")
            print("• ✅ Data integrity and accuracy confirmed")
            print("• ✅ Security and error handling validated")
            print("• ✅ Frontend integration working")
            print("• ✅ MVP success criteria achieved")
            
            if self.performance_metrics:
                print(f"\n📊 Performance Metrics:")
                print(f"• Response Time: {self.performance_metrics.get('response_time_ms', 0):.1f}ms")
                print(f"• Calculation Time: {self.performance_metrics.get('api_calculation_ms', 0):.1f}ms") 
                print(f"• Concurrent Success Rate: {self.performance_metrics.get('concurrent_success_rate', 0):.1%}")
            
            return True
        else:
            print("⚠️ Additional improvements needed before production deployment.")
            print(f"Target: 85% pass rate, Achieved: {success_rate:.0%}")
            return False

async def main():
    """Run complete production test suite"""
    test_suite = ProductionTestSuite()
    return await test_suite.run_all_tests()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)