"""
Quick test for basic API functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test if we can import core modules"""
    print("🧪 Testing basic imports...")
    
    try:
        # Test individual module imports
        from api.core.calculation_methodology import CarbonCalculationMethodology
        print("✅ CarbonCalculationMethodology imported")
        
        from api.core.carbon_engine import CarbonCalculationEngine  
        print("✅ CarbonCalculationEngine imported")
        
        from api.core.data_access import DataAccessManager
        print("✅ DataAccessManager imported")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_calculation_engine():
    """Test carbon calculation engine directly"""
    print("\n🔥 Testing Carbon Calculation Engine...")
    
    try:
        from api.core.carbon_engine import CarbonCalculationEngine
        
        # Initialize engine
        engine = CarbonCalculationEngine()
        print("✅ Engine initialized")
        
        # Test basic calculation
        result = engine.calculate_product_footprint(
            product_name="smartphone",
            quantity=1.0,
            origin_country="CHN",
            destination_country="USA", 
            transport_mode="sea_freight"
        )
        
        print(f"✅ Calculation completed!")
        print(f"   Total emissions: {result.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
        print(f"   Manufacturing: {result.get('manufacturing_emissions', 0):.2f} kg CO2e")
        print(f"   Transport: {result.get('transport_emissions', 0):.2f} kg CO2e")
        print(f"   Response time: {result.get('calculation_time_ms', 0):.1f} ms")
        
        return True
    except Exception as e:
        print(f"❌ Calculation error: {e}")
        return False

def test_data_access():
    """Test data access functionality"""
    print("\n📊 Testing Data Access...")
    
    try:
        from api.core.data_access import DataAccessManager
        
        data_manager = DataAccessManager()
        print("✅ Data manager initialized")
        
        # Test data loading
        stats = data_manager.get_performance_stats()
        print(f"✅ Data stats retrieved:")
        print(f"   Countries loaded: {stats.get('countries_loaded', 0)}")
        print(f"   Data size: {stats.get('data_size', 0)}")
        print(f"   Cache hit rate: {stats.get('cache_hit_rate', 0):.1%}")
        
        return True
    except Exception as e:
        print(f"❌ Data access error: {e}")
        return False

def run_all_tests():
    """Run all basic tests"""
    print("🚀 GreenAlpha Carbon Calculator - Basic Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Calculation Engine", test_calculation_engine), 
        ("Data Access", test_data_access)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n🎯 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Carbon Calculator is ready!")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)