"""
Quick smoke test for Carbon Calculator
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_methodology():
    """Test calculation methodology"""
    print("🧪 Testing Calculation Methodology...")
    
    try:
        from api.core.calculation_methodology import CarbonCalculationEngine
        
        # Create engine instance
        engine = CarbonCalculationEngine()
        print("✅ Calculation engine created")
        
        # Test a simple calculation
        from api.core.calculation_methodology import ProductionData, TransportationData, TransportMode
        
        # Create test data
        production = ProductionData(
            energy_intensity=85.0,  # kWh per unit
            material_footprint={"steel": 0.025, "aluminum": 0.015, "plastic_pet": 0.08},
            water_usage=12000.0,
            waste_generation=0.5
        )
        
        transport = TransportationData(
            distance_km=10000,  # China to USA approximate
            weight_kg=0.2,
            mode=TransportMode.SEA_FREIGHT
        )
        
        # Calculate footprint using unified API
        result = engine.calculate_footprint(
            production_data=production,
            transport_data=transport,
            country_code="CHN",
            quantity=1.0
        )
        
        print(f"✅ Calculation completed!")
        print(f"   Production emissions: {result.production_emissions:.2f} kg CO2e")
        print(f"   Transport emissions: {result.transport_emissions:.2f} kg CO2e") 
        print(f"   Total emissions: {result.total_emissions:.2f} kg CO2e")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_loading():
    """Test if we can load CO2 data"""
    print("\n📊 Testing Data Loading...")
    
    try:
        import pandas as pd
        
        # Try to load the CO2 data
        data_path = "../data/carbon_data.csv"
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            print(f"✅ CO2 data loaded: {len(df)} records")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Date range: {df['Year'].min()} - {df['Year'].max()}")
            
            # Sample data
            print(f"   Sample data:")
            print(f"   {df.head(2).to_string()}")
            
            return True
        else:
            print(f"❌ Data file not found: {data_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_performance():
    """Test basic performance"""
    print("\n⚡ Testing Performance...")
    
    try:
        import time
        from api.core.calculation_methodology import CarbonCalculationEngine, ProductionData, TransportationData, TransportMode
        
        engine = CarbonCalculationEngine()
        
        # Prepare test data
        production = ProductionData(
            energy_intensity=85.0,
            material_footprint={"steel": 0.025, "aluminum": 0.015, "plastic_pet": 0.08},
            water_usage=12000.0,
            waste_generation=0.5
        )
        
        transport = TransportationData(
            distance_km=10000,
            weight_kg=0.2,
            mode=TransportMode.SEA_FREIGHT
        )
        
        # Performance test - 10 calculations
        start_time = time.time()
        results = []
        
        for i in range(10):
            result = engine.calculate_footprint(
                production_data=production,
                transport_data=transport,
                country_code="CHN",
                quantity=1.0
            )
            results.append(result)
        
        end_time = time.time()
        avg_time = (end_time - start_time) * 1000 / 10  # ms per calculation
        
        print(f"✅ Performance test completed!")
        print(f"   10 calculations in {(end_time - start_time)*1000:.1f}ms")
        print(f"   Average time per calculation: {avg_time:.1f}ms")
        print(f"   Target: <500ms ✅" if avg_time < 500 else f"   Target: <500ms ❌")
        
        return avg_time < 500
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")
        return False

def main():
    """Run all quick tests"""
    print("🚀 GreenAlpha Carbon Calculator - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Calculation Methodology", test_methodology),
        ("Data Loading", test_data_loading),
        ("Performance", test_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n🎯 Quick Test Results")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    success_rate = passed / len(results)
    print(f"\nOverall: {passed}/{len(results)} tests passed ({success_rate:.0%})")
    
    if success_rate >= 0.66:  # At least 2/3 pass
        print("🎉 Carbon Calculator core functionality is working!")
        return True
    else:
        print("⚠️  Some core functionality issues detected.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)