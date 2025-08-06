"""
Quick validation test to confirm all endpoints are working
"""
import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8000"
    
    print("🚀 Starting quick validation test...")
    
    # Start server in background (assuming it's already running)
    try:
        # Test 1: Health Check
        print("\n1. Testing Health Check...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            data = health_response.json()
            print(f"   ✅ Health: {data['status']}")
            print(f"   ✅ Countries: {data['components']['data_manager']['countries_loaded']}")
            print(f"   ✅ Records: {data['components']['data_manager']['data_records']}")
        else:
            print(f"   ❌ Health check failed: {health_response.status_code}")
            return False
        
        # Test 2: Quick Carbon Calculation
        print("\n2. Testing Carbon Calculation...")
        calc_payload = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight",
            "weight_kg": 0.2
        }
        
        calc_response = requests.post(f"{base_url}/carbon/calculate", json=calc_payload, timeout=10)
        if calc_response.status_code == 200:
            data = calc_response.json()
            print(f"   ✅ Total emissions: {data['total_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"   ✅ Response time: {data['response_time_ms']:.2f}ms")
            print(f"   ✅ Confidence: {data['calculation_confidence']:.1f}%")
        else:
            print(f"   ❌ Calculation failed: {calc_response.status_code}")
            try:
                error = calc_response.json()
                print(f"   Error: {error.get('detail', 'Unknown error')}")
            except:
                print(f"   Error: {calc_response.text}")
            return False
        
        # Test 3: Global Stats
        print("\n3. Testing Global Statistics...")
        stats_response = requests.get(f"{base_url}/carbon/stats/global", timeout=5)
        if stats_response.status_code == 200:
            data = stats_response.json()
            print(f"   ✅ Global stats available: {len(data)} data points")
        else:
            print(f"   ❌ Global stats failed: {stats_response.status_code}")
            return False
        
        print("\n🎉 All quick validation tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running on localhost:8000?")
        print("   Run: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_api_endpoints()
    if success:
        print("\n✅ GreenAlpha FastAPI endpoints are ready for production!")
    else:
        print("\n❌ Some issues detected. Please check the server.")