"""
Test Suite for Supply Chain Integration Module
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.core.supply_chain_integration import (
    SupplyChainIntegrator,
    Supplier,
    SupplyChainNode,
    SupplyChainRoute
)

class TestSupplyChainIntegration(unittest.TestCase):
    """Test supply chain integration functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.integrator = SupplyChainIntegrator()
    
    def test_load_suppliers_database(self):
        """Test supplier database loading"""
        suppliers = self.integrator.suppliers_db
        self.assertIsNotNone(suppliers)
        self.assertGreater(len(suppliers), 0)
        
        # Check supplier structure
        for supplier_id, supplier in suppliers.items():
            self.assertIsInstance(supplier, Supplier)
            self.assertIsNotNone(supplier.name)
            self.assertIsNotNone(supplier.country)
            self.assertGreaterEqual(supplier.sustainability_rating, 0)
            self.assertLessEqual(supplier.sustainability_rating, 100)
    
    def test_find_suppliers(self):
        """Test finding suppliers based on criteria"""
        # Find high sustainability suppliers
        suppliers = self.integrator.find_suppliers(
            product_category="general",
            min_sustainability=80.0,
            max_carbon_intensity=3.0
        )
        
        self.assertIsNotNone(suppliers)
        for supplier in suppliers:
            self.assertGreaterEqual(supplier.sustainability_rating, 80.0)
            self.assertLessEqual(supplier.carbon_intensity, 3.0)
    
    def test_calculate_supply_chain_emissions(self):
        """Test supply chain emissions calculation"""
        result = self.integrator.calculate_supply_chain_emissions(
            origin="Shanghai",
            destination="Hamburg",
            commodity="steel",
            quantity_tons=100,
            transport_mode="maritime"
        )
        
        self.assertIsNotNone(result)
        self.assertIn("total_emissions_kg_co2e", result)
        self.assertIn("production_emissions", result)
        self.assertIn("transportation_emissions", result)
        self.assertIn("processing_emissions", result)
        
        # Check emissions are positive
        self.assertGreater(result["total_emissions_kg_co2e"], 0)
        self.assertGreater(result["production_emissions"], 0)
        self.assertGreater(result["transportation_emissions"], 0)
        
        # Check breakdown percentages sum to 100
        breakdown = result["breakdown_percentage"]
        total_percentage = sum(breakdown.values())
        self.assertAlmostEqual(total_percentage, 100.0, places=1)
    
    def test_different_transport_modes(self):
        """Test emissions for different transport modes"""
        modes = ["maritime", "rail", "road", "air"]
        emissions_by_mode = {}
        
        for mode in modes:
            result = self.integrator.calculate_supply_chain_emissions(
                origin="Shanghai",
                destination="Hamburg",
                commodity="electronics",
                quantity_tons=10,
                transport_mode=mode
            )
            emissions_by_mode[mode] = result["transportation_emissions"]
        
        # Air should have highest transport emissions
        self.assertEqual(
            max(emissions_by_mode, key=emissions_by_mode.get),
            "air"
        )
        
        # Maritime should have lowest transport emissions
        self.assertEqual(
            min(emissions_by_mode, key=emissions_by_mode.get),
            "maritime"
        )
    
    def test_optimize_supply_chain(self):
        """Test supply chain optimization"""
        # Optimize for emissions
        route = self.integrator.optimize_supply_chain(
            origin="Mumbai",
            destination="Hamburg",
            commodity="textiles",
            quantity_tons=50,
            optimization_goal="emissions"
        )
        
        self.assertIsInstance(route, SupplyChainRoute)
        self.assertGreater(len(route.nodes), 0)
        self.assertGreater(route.total_emissions, 0)
        self.assertGreater(route.total_cost, 0)
        self.assertGreater(route.total_time_days, 0)
        
        # Sustainability score should be between 0 and 100
        self.assertGreaterEqual(route.sustainability_score, 0)
        self.assertLessEqual(route.sustainability_score, 100)
    
    def test_optimization_goals(self):
        """Test different optimization goals"""
        goals = ["emissions", "cost", "time"]
        routes = {}
        
        for goal in goals:
            route = self.integrator.optimize_supply_chain(
                origin="Shanghai",
                destination="Los Angeles",
                commodity="aluminum",
                quantity_tons=75,
                optimization_goal=goal
            )
            routes[goal] = route
        
        # Different goals should potentially give different results
        self.assertIsNotNone(routes["emissions"])
        self.assertIsNotNone(routes["cost"])
        self.assertIsNotNone(routes["time"])
    
    def test_supplier_recommendations(self):
        """Test supplier recommendations"""
        recommendations = self.integrator.get_supplier_recommendations(
            commodity="steel",
            destination="Los Angeles",
            quantity_tons=100,
            max_results=3
        )
        
        self.assertIsNotNone(recommendations)
        self.assertLessEqual(len(recommendations), 3)
        
        for rec in recommendations:
            self.assertIn("supplier", rec)
            self.assertIn("emissions_analysis", rec)
            self.assertIn("optimized_route", rec)
            self.assertIn("recommendation_score", rec)
            
            # Check recommendation score is reasonable
            self.assertGreaterEqual(rec["recommendation_score"], 0)
            self.assertLessEqual(rec["recommendation_score"], 100)
        
        # Check recommendations are sorted by score
        scores = [r["recommendation_score"] for r in recommendations]
        self.assertEqual(scores, sorted(scores, reverse=True))
    
    def test_commodity_specific_factors(self):
        """Test commodity-specific emission factors"""
        commodities = ["steel", "aluminum", "textiles", "electronics"]
        results = {}
        
        for commodity in commodities:
            result = self.integrator.calculate_supply_chain_emissions(
                origin="Shanghai",
                destination="Hamburg",
                commodity=commodity,
                quantity_tons=10,
                transport_mode="maritime"
            )
            results[commodity] = result["production_emissions"]
        
        # Aluminum should have higher production emissions than steel
        self.assertGreater(results["aluminum"], results["steel"])
        
        # All should be positive
        for commodity, emissions in results.items():
            self.assertGreater(emissions, 0, f"{commodity} emissions should be positive")
    
    def test_waste_factor_application(self):
        """Test waste factor is properly applied"""
        result = self.integrator.calculate_supply_chain_emissions(
            origin="Detroit",
            destination="Los Angeles",
            commodity="electronics",
            quantity_tons=100,
            transport_mode="rail"
        )
        
        # Waste adjusted quantity should be greater than original
        self.assertGreater(result["waste_adjusted_quantity"], 100)
        
    def test_edge_cases(self):
        """Test edge cases"""
        # Test with unknown commodity
        result = self.integrator.calculate_supply_chain_emissions(
            origin="Shanghai",
            destination="Hamburg",
            commodity="unknown_commodity",
            quantity_tons=50,
            transport_mode="maritime"
        )
        self.assertIsNotNone(result)
        self.assertGreater(result["total_emissions_kg_co2e"], 0)
        
        # Test with unknown route
        result = self.integrator.calculate_supply_chain_emissions(
            origin="Unknown City",
            destination="Another Unknown",
            commodity="steel",
            quantity_tons=25,
            transport_mode="road"
        )
        self.assertIsNotNone(result)
        self.assertGreater(result["total_emissions_kg_co2e"], 0)

class TestSupplierManagement(unittest.TestCase):
    """Test supplier management functionality"""
    
    def setUp(self):
        self.integrator = SupplyChainIntegrator()
    
    def test_supplier_certifications(self):
        """Test supplier certifications"""
        suppliers = self.integrator.find_suppliers(
            product_category="general",
            min_sustainability=90.0
        )
        
        for supplier in suppliers:
            self.assertIsInstance(supplier.certifications, list)
            self.assertGreater(len(supplier.certifications), 0)
    
    def test_supplier_reliability(self):
        """Test supplier reliability scores"""
        all_suppliers = list(self.integrator.suppliers_db.values())
        
        for supplier in all_suppliers:
            self.assertGreaterEqual(supplier.reliability_score, 0)
            self.assertLessEqual(supplier.reliability_score, 100)

if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)