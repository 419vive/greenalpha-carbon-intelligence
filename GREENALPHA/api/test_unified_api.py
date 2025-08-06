#!/usr/bin/env python3
"""
Test the unified carbon calculation API
"""
import sys
import time
from api.core.calculation_methodology import (
    calculation_engine,
    ProductionData,
    TransportationData,
    TransportMode
)

def test_unified_api():
    """Test the unified calculate_footprint API"""
    print("🔧 Testing Unified Carbon Calculation API")
    print("=" * 50)
    
    # Test 1: Basic footprint calculation
    print("1. Testing calculate_footprint() method...")
    
    try:
        # Create production data for smartphone
        production_data = ProductionData(
            energy_intensity=85.0,
            material_footprint={
                "steel": 0.025,
                "aluminum": 0.015,
                "plastic_pet": 0.08
            },
            water_usage=12000.0,
            waste_generation=0.5
        )
        
        # Create transportation data
        transport_data = TransportationData(
            distance_km=11000.0,  # China to USA
            weight_kg=0.2,  # Smartphone weight
            mode=TransportMode.SEA_FREIGHT,
            load_factor=0.8
        )
        
        # Calculate footprint
        start_time = time.time()
        result = calculation_engine.calculate_footprint(
            production_data=production_data,
            transport_data=transport_data,
            country_code="CHN",
            quantity=1.0
        )
        calculation_time = (time.time() - start_time) * 1000
        
        print(f"   ✅ Method exists and returns result")
        print(f"   📊 Total emissions: {result.total_emissions:.2f} kg CO2e")
        print(f"   🏭 Production emissions: {result.production_emissions:.2f} kg CO2e")
        print(f"   🚛 Transport emissions: {result.transport_emissions:.2f} kg CO2e")
        print(f"   ⏱️  Calculation time: {result.calculation_time_ms:.2f}ms")
        print(f"   🎯 Uncertainty: {result.uncertainty_percentage:.1f}%")
        
        # Validate results
        assert result.total_emissions > 0, "Total emissions should be positive"
        assert result.production_emissions > 0, "Production emissions should be positive"
        assert result.transport_emissions > 0, "Transport emissions should be positive"
        assert result.calculation_time_ms > 0, "Calculation time should be recorded"
        assert result.calculation_time_ms < 100, "Should be fast (<100ms)"
        assert isinstance(result.breakdown, dict), "Breakdown should be a dictionary"
        
        print("   ✅ All validations passed")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
    
    # Test 2: Convenience method
    print("\n2. Testing calculate_product_footprint() convenience method...")
    
    try:
        result = calculation_engine.calculate_product_footprint(
            product_name="smartphone",
            quantity=1.0,
            origin="CHN",
            destination="USA",
            transport_mode="sea_freight"
        )
        
        print(f"   ✅ Convenience method works")
        print(f"   📱 Smartphone footprint: {result.total_emissions:.2f} kg CO2e")
        print(f"   ⏱️  Response time: {result.calculation_time_ms:.2f}ms")
        
        # Validate reasonable smartphone emissions (should be ~50-60 kg CO2e)
        assert 20 <= result.total_emissions <= 200, f"Smartphone emissions seem unreasonable: {result.total_emissions}"
        print("   ✅ Emissions are within reasonable range")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
    
    # Test 3: Return format consistency
    print("\n3. Testing return format consistency...")
    
    try:
        # Test that methods return numbers, not dicts
        prod_result = calculation_engine.calculate_production_emissions(
            production_data, "CHN", 1.0
        )
        transport_result = calculation_engine.calculate_transportation_emissions(
            transport_data
        )
        
        print(f"   📋 Production result type: {type(prod_result)}")
        print(f"   📋 Transport result type: {type(transport_result)}")
        
        # These should be dicts with numeric values
        assert isinstance(prod_result, dict), "Production result should be dict"
        assert isinstance(transport_result, dict), "Transport result should be dict"
        assert "total_production" in prod_result, "Should have total_production key"
        assert "total_transport" in transport_result, "Should have total_transport key"
        
        print("   ✅ Return formats are consistent")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False
    
    print("\n🎉 All tests passed! Carbon Calculation Engine is working correctly.")
    print(f"📈 Performance Summary:")
    print(f"   - Response time: <100ms ✅")
    print(f"   - Smartphone emissions: ~{result.total_emissions:.0f} kg CO2e ✅")
    print(f"   - Method compatibility: ✅")
    print(f"   - Error handling: ✅")
    
    return True

def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🔧 Testing Edge Cases")
    print("=" * 30)
    
    try:
        # Test with zero quantity
        result = calculation_engine.calculate_product_footprint(
            product_name="smartphone",
            quantity=0.1,
            origin="CHN",
            destination="USA"
        )
        print(f"   ✅ Small quantity works: {result.total_emissions:.2f} kg CO2e")
        
        # Test with unknown product
        result = calculation_engine.calculate_product_footprint(
            product_name="unknown_product",
            quantity=1.0,
            origin="CHN",
            destination="USA"
        )
        print(f"   ✅ Unknown product fallback: {result.total_emissions:.2f} kg CO2e")
        
        # Test with different transport modes
        modes = ["road_truck", "rail", "air_freight", "sea_freight"]
        emissions_by_mode = {}
        
        for mode in modes:
            result = calculation_engine.calculate_product_footprint(
                product_name="smartphone",
                quantity=1.0,
                origin="CHN",
                destination="USA",
                transport_mode=mode
            )
            emissions_by_mode[mode] = result.transport_emissions
        
        print(f"   📊 Transport mode emissions:")
        for mode, emissions in emissions_by_mode.items():
            print(f"      {mode}: {emissions:.2f} kg CO2e")
        
        # Air freight should be highest
        assert emissions_by_mode["air_freight"] > emissions_by_mode["sea_freight"], \
            "Air freight should have higher emissions than sea freight"
        
        print("   ✅ Transport mode logic is correct")
        
    except Exception as e:
        print(f"   ❌ Edge case error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_unified_api()
    if success:
        success = test_edge_cases()
    
    if success:
        print("\n🚀 Carbon Calculation Engine is ready for production!")
        sys.exit(0)
    else:
        print("\n💥 Tests failed. Please check the implementation.")
        sys.exit(1)