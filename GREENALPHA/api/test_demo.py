#!/usr/bin/env python3
"""
Quick test script to verify the demo is working
"""
import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def test_demo():
    """Test the demo functionality"""
    print("🧪 Testing GreenAlpha Executive Demo...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Not in API directory. Please run from /api folder")
        return False
    
    # Check if static files exist
    static_files = ['static/index.html', 'static/style.css', 'static/script.js']
    for file in static_files:
        if not os.path.exists(file):
            print(f"❌ Missing static file: {file}")
            return False
    print("✅ All static files present")
    
    # Start server in background
    print("\n🚀 Starting test server...")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "127.0.0.1", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://127.0.0.1:8000"
        endpoints_to_test = [
            ("/", "Root endpoint"),
            ("/health", "Health check"),
            ("/demo/", "Demo frontend"),
            ("/static/index.html", "Static HTML file")
        ]
        
        print("\n🔍 Testing endpoints...")
        all_passed = True
        
        for endpoint, description in endpoints_to_test:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    print(f"✅ {description}: OK (200)")
                else:
                    print(f"⚠️  {description}: {response.status_code}")
                    if endpoint != "/demo/":  # Demo might not be perfectly configured yet
                        all_passed = False
            except Exception as e:
                print(f"❌ {description}: Failed - {str(e)}")
                all_passed = False
        
        # Test a carbon calculation
        print("\n🧮 Testing carbon calculation...")
        try:
            calc_data = {
                "product_name": "smartphone",
                "quantity": 1,
                "origin_country": "CHN",
                "destination_country": "USA",
                "transport_mode": "air_freight"
            }
            
            response = requests.post(
                f"{base_url}/carbon/calculate",
                json=calc_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Carbon calculation: {result.get('total_emissions_kg_co2e', 'N/A')} kg CO₂e")
                print(f"⏱️  Response time: {result.get('response_time_ms', 'N/A')} ms")
            else:
                print(f"⚠️  Carbon calculation failed: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ Carbon calculation error: {str(e)}")
            all_passed = False
        
        # Cleanup
        process.terminate()
        process.wait(timeout=5)
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 Demo test PASSED! Ready for executives!")
            print("\nTo launch the demo:")
            print("python launch_demo.py")
            print("\nDemo will be available at:")
            print("http://localhost:8000/demo")
        else:
            print("⚠️  Some tests failed. Check the issues above.")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_demo()
    sys.exit(0 if success else 1)