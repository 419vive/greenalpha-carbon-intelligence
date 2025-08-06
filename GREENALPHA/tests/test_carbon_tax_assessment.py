"""
Tests for carbon tax assessment functionality
"""
import unittest
import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.core.carbon_tax_assessment import (
    CarbonTaxAssessor,
    TaxJurisdiction,
    CarbonTaxPolicy,
    TaxAssessmentResult
)


class TestCarbonTaxAssessment(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tax_assessor = CarbonTaxAssessor()
        
    def test_initialization(self):
        """Test that CarbonTaxAssessor initializes correctly."""
        self.assertIsInstance(self.tax_assessor, CarbonTaxAssessor)
        
    def test_calculate_carbon_tax_basic(self):
        """Test basic carbon tax calculation."""
        # Test with sample data
        emissions = 1000  # tonnes CO2
        country_code = "US"
        year = 2024
        
        result = self.tax_assessor.calculate_tax(emissions, country_code, year)
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_tax', result)
        self.assertIn('tax_rate', result)
        self.assertIn('currency', result)
        
    def test_calculate_carbon_tax_multiple_countries(self):
        """Test carbon tax calculation for multiple countries."""
        test_cases = [
            {"emissions": 1000, "country": "EU", "year": 2024},
            {"emissions": 500, "country": "UK", "year": 2024},
            {"emissions": 2000, "country": "CA", "year": 2024},
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                result = self.tax_assessor.calculate_tax(
                    case["emissions"], 
                    case["country"], 
                    case["year"]
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(result.get('total_tax', 0), 0)
                
    def test_get_tax_rates(self):
        """Test retrieving tax rates by country."""
        rates = self.tax_assessor.get_tax_rates("EU", 2024)
        
        self.assertIsInstance(rates, dict)
        self.assertIn('rate', rates)
        self.assertIn('currency', rates)
        
    def test_invalid_country_code(self):
        """Test handling of invalid country codes."""
        result = self.tax_assessor.calculate_tax(1000, "INVALID", 2024)
        
        # Should either return default rate or handle gracefully
        self.assertIsInstance(result, dict)
        
    def test_zero_emissions(self):
        """Test calculation with zero emissions."""
        result = self.tax_assessor.calculate_tax(0, "US", 2024)
        
        self.assertEqual(result.get('total_tax', 0), 0)
        
    def test_negative_emissions(self):
        """Test handling of negative emissions (carbon credits)."""
        result = self.tax_assessor.calculate_tax(-500, "EU", 2024)
        
        # Should handle negative emissions appropriately
        self.assertIsInstance(result, dict)
        
    def test_future_year(self):
        """Test calculation for future years."""
        result = self.tax_assessor.calculate_tax(1000, "US", 2030)
        
        self.assertIsInstance(result, dict)
        
    def test_historical_year(self):
        """Test calculation for historical years."""
        result = self.tax_assessor.calculate_tax(1000, "EU", 2020)
        
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()