#!/usr/bin/env python3
"""
Frontend Integration Test
Tests the complete frontend-to-API integration
"""
import requests
import json
import time
from datetime import datetime

def test_api_health():
    """Test API health endpoint"""
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print(f"❌ API Health Check: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ API Health Check: FAILED ({e})")
        return False

def test_carbon_calculation():
    """Test carbon calculation endpoint"""
    test_cases = [
        {
            'name': 'Smartphone China->USA (Air)',
            'request': {
                'product_name': 'smartphone',
                'quantity': 1,
                'origin_country': 'CHN',
                'destination_country': 'USA',
                'transport_mode': 'air_freight'
            }
        },
        {
            'name': 'Laptop Germany->Japan (Sea)',
            'request': {
                'product_name': 'laptop',
                'quantity': 1,
                'origin_country': 'DEU',
                'destination_country': 'JPN',
                'transport_mode': 'sea_freight'
            }
        },
        {
            'name': 'T-shirt India->UK (Sea)',
            'request': {
                'product_name': 't-shirt',
                'quantity': 1,
                'origin_country': 'IND',
                'destination_country': 'GBR',
                'transport_mode': 'sea_freight'
            }
        }
    ]
    
    print("\n🧪 Testing Carbon Calculation Scenarios:")
    print("-" * 50)
    
    all_passed = True
    
    for test_case in test_cases:
        try:
            start_time = time.time()
            
            response = requests.post(
                'http://localhost:8000/carbon/calculate',
                json=test_case['request'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                total_emissions = result.get('total_emissions_kg_co2e', 0)
                server_time = result.get('response_time_ms', 0)
                
                print(f"✅ {test_case['name']}")
                print(f"   Total Emissions: {total_emissions:.2f} kg CO2e")
                print(f"   Response Time: {response_time:.1f}ms (server: {server_time:.1f}ms)")
                
                # Validate response structure
                required_fields = [
                    'total_emissions_kg_co2e', 'production_emissions', 
                    'transportation_emissions', 'carbon_cost_usd',
                    'calculation_confidence', 'response_time_ms'
                ]
                
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    print(f"   ⚠️  Missing fields: {missing_fields}")
                    all_passed = False
                
                if response_time > 500:
                    print(f"   ⚠️  Response time exceeded 500ms target")
                
            else:
                print(f"❌ {test_case['name']}: FAILED ({response.status_code})")
                print(f"   Error: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {test_case['name']}: EXCEPTION ({e})")
            all_passed = False
    
    return all_passed

def test_frontend_files():
    """Test that frontend files are accessible"""
    try:
        response = requests.get('http://localhost:8000/demo/', timeout=5)
        if response.status_code == 200 and 'GreenAlpha' in response.text:
            print("✅ Frontend Access: PASSED")
            return True
        else:
            print(f"❌ Frontend Access: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Frontend Access: FAILED ({e})")
        return False

def main():
    """Run all integration tests"""
    print("🚀 GreenAlpha Frontend Integration Test")
    print("=" * 50)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("API Health", test_api_health),
        ("Frontend Files", test_frontend_files),
        ("Carbon Calculations", test_carbon_calculation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} Test...")
        results[test_name] = test_func()
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Frontend is ready for executives.")
        print("\n🌐 Access the demo at: http://localhost:8000/demo/")
    else:
        print("⚠️  SOME TESTS FAILED! Please check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)