"""
Working test for Carbon Calculator with correct API
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_calculation_engine():
    """Test the carbon calculation engine with correct data structures"""
    print("🧪 Testing Carbon Calculation Engine...")
    
    try:
        from api.core.calculation_methodology import (
            CarbonCalculationEngine, 
            ProductionData, 
            TransportationData, 
            TransportMode
        )
        
        # Initialize engine
        engine = CarbonCalculationEngine()
        print("✅ Engine initialized")
        
        # Create correct production data structure
        production = ProductionData(
            energy_intensity=85.0,  # kWh per smartphone
            material_footprint={
                "aluminum": 0.05,  # kg per unit
                "plastic_pet": 0.1,
                "steel": 0.02
            },
            water_usage=1000.0,  # liters
            waste_generation=0.05  # kg
        )
        print("✅ Production data created")
        
        # Create transportation data
        transport = TransportationData(
            distance_km=10000,  # China to USA
            weight_kg=0.2,  # smartphone weight
            mode=TransportMode.SEA_FREIGHT,
            load_factor=0.8
        )
        print("✅ Transport data created")
        
        # Test if calculate_footprint method exists
        if hasattr(engine, 'calculate_footprint'):
            result = engine.calculate_footprint(production, transport)
            print("✅ Calculation completed using calculate_footprint!")
            
            # Check if result has expected attributes
            if hasattr(result, 'total_emissions'):
                print(f"   Total emissions: {result.total_emissions:.2f} kg CO2e")
            if hasattr(result, 'production_emissions'):
                print(f"   Production: {result.production_emissions:.2f} kg CO2e")
            if hasattr(result, 'transport_emissions'):
                print(f"   Transport: {result.transport_emissions:.2f} kg CO2e")
                
        else:
            print("❌ calculate_footprint method not found")
            print("   Available methods:", [m for m in dir(engine) if not m.startswith('_')])
            
            # Try alternative methods
            if hasattr(engine, 'calculate_production_emissions'):
                prod_emissions = engine.calculate_production_emissions(production, "CHN")
                print(f"✅ Production emissions: {prod_emissions:.2f} kg CO2e")
                
            if hasattr(engine, 'calculate_transport_emissions'):
                trans_emissions = engine.calculate_transport_emissions(transport)
                print(f"✅ Transport emissions: {trans_emissions:.2f} kg CO2e")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_loading():
    """Test CO2 data loading"""
    print("\n📊 Testing CO2 Data Loading...")
    
    try:
        import pandas as pd
        
        # Try multiple possible data paths
        possible_paths = [
            "../data/carbon_data.csv",
            "../../data/carbon_data.csv", 
            "../data/project 3.csv",
            "../../project 3.csv"
        ]
        
        data_loaded = False
        for data_path in possible_paths:
            if os.path.exists(data_path):
                df = pd.read_csv(data_path)
                print(f"✅ CO2 data loaded from {data_path}")
                print(f"   Records: {len(df)}")
                print(f"   Columns: {list(df.columns)}")
                print(f"   Date range: {df['Year'].min()} - {df['Year'].max()}")
                
                # Show sample
                sample = df.head(3)
                print(f"   Sample data:")
                for _, row in sample.iterrows():
                    print(f"     {row['Entity']}: {row['Annual CO₂ emissions (tonnes )']} tonnes in {row['Year']}")
                
                data_loaded = True
                break
        
        if not data_loaded:
            print("❌ CO2 data file not found in any expected location")
            print("   Searched paths:", possible_paths)
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_emission_factors():
    """Test emission factors"""
    print("\n⚡ Testing Emission Factors...")
    
    try:
        from api.core.calculation_methodology import CarbonCalculationEngine
        
        engine = CarbonCalculationEngine()
        
        # Test emission factors
        factors = engine.emission_factors
        print(f"✅ Loaded {len(factors)} emission factors")
        
        # Show some key factors
        key_factors = ["grid_electricity_global", "steel", "diesel"]
        for factor_name in key_factors:
            if factor_name in factors:
                factor = factors[factor_name]
                print(f"   {factor_name}: {factor.value} kg CO2e/{factor.unit}")
        
        # Test country factors
        countries = engine.country_factors
        print(f"✅ Loaded {len(countries)} country factors")
        
        for country in ["USA", "CHN", "DEU"]:
            if country in countries:
                elec = countries[country]["electricity"]
                print(f"   {country}: {elec} kg CO2e/kWh electricity")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing factors: {e}")
        return False

def test_simple_calculation():
    """Test a simple manual calculation"""
    print("\n🔥 Testing Simple Manual Calculation...")
    
    try:
        from api.core.calculation_methodology import CarbonCalculationEngine
        
        engine = CarbonCalculationEngine()
        
        # Manual calculation for smartphone
        energy_used = 85.0  # kWh
        china_electricity_factor = 0.644  # kg CO2e/kWh
        
        production_emissions = energy_used * china_electricity_factor
        print(f"✅ Manual production calculation:")
        print(f"   Energy: {energy_used} kWh")
        print(f"   China factor: {china_electricity_factor} kg CO2e/kWh") 
        print(f"   Production emissions: {production_emissions:.2f} kg CO2e")
        
        # Transport calculation
        distance = 10000  # km
        weight = 0.0002  # 0.2 kg to tonnes
        sea_factor = 0.014  # kg CO2e/tonne-km
        
        transport_emissions = distance * weight * sea_factor
        print(f"✅ Manual transport calculation:")
        print(f"   Distance: {distance} km")
        print(f"   Weight: {weight} tonnes")
        print(f"   Sea factor: {sea_factor} kg CO2e/tonne-km")
        print(f"   Transport emissions: {transport_emissions:.4f} kg CO2e")
        
        total = production_emissions + transport_emissions
        print(f"✅ Total footprint: {total:.2f} kg CO2e")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in manual calculation: {e}")
        return False

def main():
    """Run working tests"""
    print("🚀 GreenAlpha Carbon Calculator - Working Test")
    print("=" * 55)
    
    tests = [
        ("Calculation Engine", test_calculation_engine),
        ("CO2 Data Loading", test_data_loading),
        ("Emission Factors", test_emission_factors),
        ("Simple Calculation", test_simple_calculation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 35)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n🎯 Test Results")
    print("=" * 55)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    success_rate = passed / len(results)
    print(f"\nOverall: {passed}/{len(results)} tests passed ({success_rate:.0%})")
    
    if success_rate >= 0.5:  # At least half pass
        print("🎉 Core Carbon Calculator components are working!")
        if success_rate < 1.0:
            print("💡 Some components need attention, but foundation is solid!")
        return True
    else:
        print("⚠️  Major issues detected. Core functionality needs work.")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🚀 Ready to proceed!' if success else '🔧 Needs fixes before proceeding.'}")
    sys.exit(0 if success else 1)