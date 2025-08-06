"""
Carbon Calculator API Usage Examples
Demonstrates various calculation scenarios and API features
"""
import asyncio
import httpx
import json
import time
from typing import Dict, List, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_HEADERS = {"Content-Type": "application/json"}

class CarbonCalculatorClient:
    """Client for interacting with Carbon Calculator API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def calculate_carbon_footprint(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate carbon footprint for a single product"""
        url = f"{self.base_url}/carbon/calculate"
        response = await self.client.post(url, json=request_data)
        response.raise_for_status()
        return response.json()
    
    async def calculate_batch(self, calculations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate carbon footprint for multiple products"""
        url = f"{self.base_url}/carbon/calculate/batch"
        request_data = {
            "calculations": calculations,
            "include_summary": True
        }
        response = await self.client.post(url, json=request_data)
        response.raise_for_status()
        return response.json()
    
    async def get_country_factors(self, country_code: str) -> Dict[str, Any]:
        """Get country-specific emission factors"""
        url = f"{self.base_url}/carbon/factors/country/{country_code}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def search_countries(self, query: str) -> Dict[str, Any]:
        """Search for countries"""
        url = f"{self.base_url}/carbon/countries/search"
        params = {"query": query}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_global_stats(self) -> Dict[str, Any]:
        """Get global carbon emission statistics"""
        url = f"{self.base_url}/carbon/stats/global"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

async def example_1_basic_smartphone_calculation():
    """Example 1: Basic smartphone calculation from China to USA"""
    print("\\n=== Example 1: Basic Smartphone Calculation ===")
    
    client = CarbonCalculatorClient()
    
    request_data = {
        "product_name": "smartphone",
        "quantity": 1.0,
        "origin_country": "CHN",
        "destination_country": "USA",
        "transport_mode": "sea_freight"
    }
    
    try:
        result = await client.calculate_carbon_footprint(request_data)
        
        print(f"Product: {request_data['product_name']}")
        print(f"Route: {request_data['origin_country']} → {request_data['destination_country']}")
        print(f"Transport: {request_data['transport_mode']}")
        print(f"\\nResults:")
        print(f"  Total Emissions: {result['total_emissions_kg_co2e']:.2f} kg CO2e")
        print(f"  Production: {result['production_emissions']:.2f} kg CO2e")
        print(f"  Transportation: {result['transportation_emissions']:.2f} kg CO2e")
        print(f"  Carbon Cost: ${result['carbon_cost_usd']:.2f}")
        print(f"  Confidence: {result['calculation_confidence']:.1f}%")
        print(f"  Response Time: {result['response_time_ms']:.2f}ms")
        
        # Show scope breakdown
        print(f"\\nScope Breakdown:")
        print(f"  Scope 1 (Direct): {result['scope_1_emissions']:.2f} kg CO2e")
        print(f"  Scope 2 (Electricity): {result['scope_2_emissions']:.2f} kg CO2e")
        print(f"  Scope 3 (Value Chain): {result['scope_3_emissions']:.2f} kg CO2e")
        
        # Show recommendations
        if result.get('recommendations'):
            print(f"\\nRecommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"  {i}. {rec['action']} ({rec['category']})")
                print(f"     Potential reduction: {rec['potential_reduction']}")
    
    finally:
        await client.close()

async def example_2_transport_mode_comparison():
    """Example 2: Compare different transport modes"""
    print("\\n=== Example 2: Transport Mode Comparison ===")
    
    client = CarbonCalculatorClient()
    
    base_request = {
        "product_name": "laptop",
        "quantity": 1.0,
        "origin_country": "TWN",
        "destination_country": "DEU"
    }
    
    transport_modes = ["sea_freight", "air_freight", "road_truck", "rail"]
    results = {}
    
    try:
        print(f"Product: {base_request['product_name']}")
        print(f"Route: {base_request['origin_country']} → {base_request['destination_country']}")
        print(f"\\nTransport Mode Comparison:")
        
        for mode in transport_modes:
            request_data = {**base_request, "transport_mode": mode}
            result = await client.calculate_carbon_footprint(request_data)
            results[mode] = result
            
            print(f"\\n{mode.replace('_', ' ').title()}:")
            print(f"  Total: {result['total_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"  Transport: {result['transportation_emissions']:.2f} kg CO2e")
            print(f"  Cost: ${result['carbon_cost_usd']:.2f}")
            print(f"  Time: {result['response_time_ms']:.2f}ms")
        
        # Find most efficient option
        most_efficient = min(results.items(), key=lambda x: x[1]['total_emissions_kg_co2e'])
        print(f"\\nMost Efficient: {most_efficient[0].replace('_', ' ').title()}")
        print(f"  Emissions: {most_efficient[1]['total_emissions_kg_co2e']:.2f} kg CO2e")
    
    finally:
        await client.close()

async def example_3_precise_coordinates():
    """Example 3: Using precise coordinates for distance calculation"""
    print("\\n=== Example 3: Precise Coordinate Calculation ===")
    
    client = CarbonCalculatorClient()
    
    # Specific locations: Apple Park (Cupertino) to Berlin
    request_data = {
        "product_name": "smartphone",
        "quantity": 100.0,  # Bulk shipment
        "origin_country": "USA",
        "destination_country": "DEU",
        "transport_mode": "air_freight",
        "origin_latitude": 37.3349,    # Apple Park, Cupertino
        "origin_longitude": -122.0090,
        "destination_latitude": 52.5200,  # Berlin
        "destination_longitude": 13.4050,
        "weight_kg": 20.0  # Specify exact weight
    }
    
    try:
        result = await client.calculate_carbon_footprint(request_data)
        
        print(f"Bulk shipment: {request_data['quantity']} smartphones")
        print(f"From: Apple Park, Cupertino ({request_data['origin_latitude']}, {request_data['origin_longitude']})")
        print(f"To: Berlin ({request_data['destination_latitude']}, {request_data['destination_longitude']})")
        print(f"Weight: {request_data['weight_kg']} kg")
        
        print(f"\\nResults:")
        print(f"  Total Emissions: {result['total_emissions_kg_co2e']:.2f} kg CO2e")
        print(f"  Per Unit: {result['total_emissions_kg_co2e']/request_data['quantity']:.2f} kg CO2e")
        print(f"  Carbon Cost: ${result['carbon_cost_usd']:.2f}")
        print(f"  Confidence: {result['calculation_confidence']:.1f}%")
        
        # Show detailed breakdown
        print(f"\\nDetailed Breakdown:")
        for key, value in result['production_breakdown'].items():
            if isinstance(value, dict):
                print(f"  {key.replace('_', ' ').title()}:")
                for subkey, subvalue in value.items():
                    print(f"    {subkey}: {subvalue:.2f} kg CO2e")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value:.2f} kg CO2e")
    
    finally:
        await client.close()

async def example_4_custom_emission_factors():
    """Example 4: Using custom emission factors"""
    print("\\n=== Example 4: Custom Emission Factors ===")
    
    client = CarbonCalculatorClient()
    
    # Standard calculation
    base_request = {
        "product_name": "laptop",
        "quantity": 1.0,
        "origin_country": "CHN",
        "destination_country": "USA",
        "transport_mode": "sea_freight"
    }
    
    # Custom calculation with eco-friendly materials
    custom_request = {
        **base_request,
        "custom_emission_factors": {
            "aluminum": 8.0,  # Lower than standard (recycled aluminum)
            "steel": 1.5,     # Lower than standard (green steel)
        }
    }
    
    try:
        print("Comparing standard vs. eco-friendly materials:")
        
        # Standard calculation
        standard_result = await client.calculate_carbon_footprint(base_request)
        print(f"\\nStandard Materials:")
        print(f"  Production: {standard_result['production_emissions']:.2f} kg CO2e")
        print(f"  Total: {standard_result['total_emissions_kg_co2e']:.2f} kg CO2e")
        
        # Custom calculation
        custom_result = await client.calculate_carbon_footprint(custom_request)
        print(f"\\nEco-Friendly Materials:")
        print(f"  Production: {custom_result['production_emissions']:.2f} kg CO2e")
        print(f"  Total: {custom_result['total_emissions_kg_co2e']:.2f} kg CO2e")
        
        # Calculate savings
        production_savings = standard_result['production_emissions'] - custom_result['production_emissions']
        total_savings = standard_result['total_emissions_kg_co2e'] - custom_result['total_emissions_kg_co2e']
        savings_percentage = (total_savings / standard_result['total_emissions_kg_co2e']) * 100
        
        print(f"\\nSavings with Eco-Friendly Materials:")
        print(f"  Production Savings: {production_savings:.2f} kg CO2e")
        print(f"  Total Savings: {total_savings:.2f} kg CO2e ({savings_percentage:.1f}%)")
    
    finally:
        await client.close()

async def example_5_batch_calculation():
    """Example 5: Batch calculation for supply chain analysis"""
    print("\\n=== Example 5: Batch Supply Chain Analysis ===")
    
    client = CarbonCalculatorClient()
    
    # Simulate a tech company's product shipments
    calculations = [
        {
            "product_name": "smartphone",
            "quantity": 1000.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        },
        {
            "product_name": "laptop",
            "quantity": 500.0,
            "origin_country": "TWN",
            "destination_country": "USA",
            "transport_mode": "air_freight"
        },
        {
            "product_name": "smartphone",
            "quantity": 800.0,
            "origin_country": "CHN",
            "destination_country": "DEU",
            "transport_mode": "sea_freight"
        },
        {
            "product_name": "laptop",
            "quantity": 300.0,
            "origin_country": "TWN",
            "destination_country": "GBR",
            "transport_mode": "air_freight"
        }
    ]
    
    try:
        print("Supply Chain Carbon Footprint Analysis")
        print(f"Calculating {len(calculations)} shipments...")
        
        start_time = time.time()
        result = await client.calculate_batch(calculations)
        batch_time = (time.time() - start_time) * 1000
        
        print(f"\\nBatch Processing Results:")
        print(f"  Processing Time: {batch_time:.2f}ms")
        print(f"  Successful Calculations: {result['successful_calculations']}")
        print(f"  Failed Calculations: {result['failed_calculations']}")
        
        if result['summary']:
            summary = result['summary']
            print(f"\\nSupply Chain Summary:")
            print(f"  Total Emissions: {summary['total_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"  Average per Shipment: {summary['average_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"  Total Carbon Cost: ${summary['total_carbon_cost_usd']:.2f}")
            print(f"  Range: {summary['min_emissions_kg_co2e']:.2f} - {summary['max_emissions_kg_co2e']:.2f} kg CO2e")
        
        # Show individual results
        print(f"\\nIndividual Shipment Results:")
        for i, shipment_result in enumerate(result['results'], 1):
            calc = calculations[shipment_result['index']]
            res = shipment_result['result']
            print(f"  {i}. {calc['product_name']} x{calc['quantity']} ({calc['origin_country']}→{calc['destination_country']}):")
            print(f"     Emissions: {res['total_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"     Cost: ${res['carbon_cost_usd']:.2f}")
    
    finally:
        await client.close()

async def example_6_country_analysis():
    """Example 6: Country-specific analysis"""
    print("\\n=== Example 6: Country Analysis ===")
    
    client = CarbonCalculatorClient()
    
    try:
        # Search for Asian countries
        print("Searching for Asian manufacturing hubs:")
        search_results = await client.search_countries("China")
        
        if search_results['results']:
            for country in search_results['results'][:3]:
                print(f"\\n{country['name']} ({country['code']}):")
                print(f"  Total Emissions: {country['total_emissions']:,.0f} tonnes CO2")
                
                # Get detailed country factors
                factors = await client.get_country_factors(country['code'])
                print(f"  Electricity Factor: {factors['electricity_factor']:.3f} kg CO2/kWh")
                print(f"  Per Capita: {factors['per_capita_emissions']:.2f} tonnes CO2/person")
                
                if factors['energy_mix']:
                    print(f"  Energy Mix: {factors['energy_mix']}")
        
        # Global statistics
        print("\\n" + "="*50)
        global_stats = await client.get_global_stats()
        print(f"Global Carbon Statistics:")
        print(f"  Countries Covered: {global_stats['total_countries']}")
        print(f"  Global Emissions: {global_stats['global_emissions']:,.0f} tonnes CO2")
        print(f"  Data Coverage: {global_stats['data_coverage']['years']}")
        
        print(f"\\nTop 5 Emitters:")
        for i, emitter in enumerate(global_stats['top_emitters'][:5], 1):
            print(f"  {i}. {emitter['country']} ({emitter['code']}): {emitter['emissions']:,.0f} tonnes")
    
    finally:
        await client.close()

async def example_7_performance_monitoring():
    """Example 7: Performance monitoring and optimization"""
    print("\\n=== Example 7: Performance Monitoring ===")
    
    client = CarbonCalculatorClient()
    
    try:
        # Make several requests to generate performance data
        print("Making multiple requests to test performance...")
        
        request_data = {
            "product_name": "smartphone",
            "quantity": 1.0,
            "origin_country": "CHN",
            "destination_country": "USA",
            "transport_mode": "sea_freight"
        }
        
        response_times = []
        for i in range(10):
            start_time = time.time()
            result = await client.calculate_carbon_footprint(request_data)
            response_time = (time.time() - start_time) * 1000
            response_times.append(response_time)
            
            if i == 0:
                api_response_time = result['response_time_ms']
            
            print(f"  Request {i+1}: {response_time:.2f}ms")
        
        # Calculate statistics
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"\\nPerformance Summary:")
        print(f"  Average Response Time: {avg_time:.2f}ms")
        print(f"  Min Response Time: {min_time:.2f}ms")
        print(f"  Max Response Time: {max_time:.2f}ms")
        print(f"  API Internal Time: {api_response_time:.2f}ms")
        print(f"  Target: <500ms ✓" if avg_time < 500 else f"  Target: <500ms ✗")
        
        # Get API performance stats
        perf_response = await client.client.get(f"{client.base_url}/carbon/stats/performance")
        if perf_response.status_code == 200:
            perf_data = perf_response.json()
            if 'engine_performance' in perf_data:
                engine_stats = perf_data['engine_performance']
                print(f"\\nEngine Performance:")
                if 'avg_response_time_ms' in engine_stats:
                    print(f"  Engine Avg Time: {engine_stats['avg_response_time_ms']:.2f}ms")
                if 'total_calculations' in engine_stats:
                    print(f"  Total Calculations: {engine_stats['total_calculations']}")
    
    finally:
        await client.close()

async def main():
    """Run all examples"""
    print("🌱 Carbon Calculator API Examples")
    print("=" * 50)
    
    try:
        # Check if API is running
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/health")
            if response.status_code != 200:
                print("❌ API is not running. Please start the API server first.")
                return
            print("✅ API server is running")
        
        # Run examples
        await example_1_basic_smartphone_calculation()
        await example_2_transport_mode_comparison()
        await example_3_precise_coordinates()
        await example_4_custom_emission_factors()
        await example_5_batch_calculation()
        await example_6_country_analysis()
        await example_7_performance_monitoring()
        
        print("\\n" + "=" * 50)
        print("🎉 All examples completed successfully!")
        
    except httpx.ConnectError:
        print("❌ Cannot connect to API. Please ensure the server is running at", API_BASE_URL)
    except Exception as e:
        print(f"❌ Error running examples: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())