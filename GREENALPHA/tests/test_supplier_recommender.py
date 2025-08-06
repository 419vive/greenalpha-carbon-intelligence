"""
Tests for the Supplier Recommender.

This test suite validates the functionality of the SupplierRecommender,
including MCDA scoring and machine learning-based similarity matching.
"""
import unittest
import sys
import os
import pandas as pd

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from api.core.supplier_recommender import SupplierRecommender, MOCK_SUPPLIERS_DF

class TestSupplierRecommender(unittest.TestCase):
    """
    Tests the core functionality of the SupplierRecommender.
    """

    def setUp(self):
        """Set up a SupplierRecommender instance for each test."""
        self.recommender = SupplierRecommender(suppliers_df=pd.DataFrame(MOCK_SUPPLIERS_DF))

    def test_initialization(self):
        """Test that the recommender initializes correctly."""
        self.assertIsNotNone(self.recommender)
        self.assertEqual(len(self.recommender.suppliers), 6) # Now 6 suppliers
        self.assertIsNotNone(self.recommender.nn_model)

    def test_mcda_recommendation_balanced(self):
        """Test MCDA recommendation with a balanced weighting."""
        weights = {
            'esg_score': 0.40,
            'cost_index': 0.30,
            'reliability_score': 0.20,
            'geographic_proximity': 0.10
        }
        result = self.recommender.recommend_by_mcda(weights, top_n=3)
        
        recommended_ids = [s['supplier_id'] for s in result.recommended_suppliers]
        # Based on the new data and weights, S006 is a top contender
        self.assertEqual(recommended_ids[0], 'S006')
        self.assertEqual(len(recommended_ids), 3)

    def test_non_compliant_supplier_penalty(self):
        """Test that a non-compliant supplier is penalized."""
        weights = {
            'esg_score': 0.8, # High ESG weight to make S003 a contender
            'cost_index': 0.1,
            'reliability_score': 0.1
        }
        
        # S003 is non-compliant and should be penalized.
        # Without penalty, S003 might rank high due to high reliability and low cost.
        result = self.recommender.recommend_by_mcda(weights, top_n=5)
        recommended_suppliers = result.recommended_suppliers
        
        s003_supplier = next((s for s in recommended_suppliers if s['supplier_id'] == 'S003'), None)
        s002_supplier = next((s for s in recommended_suppliers if s['supplier_id'] == 'S002'), None)

        self.assertIsNotNone(s003_supplier)
        self.assertIsNotNone(s002_supplier)
        
        # Even with high ESG focus, S003's penalty should lower its rank
        self.assertLess(s003_supplier['mcda_score'], s002_supplier['mcda_score'])

    def test_find_similar_suppliers(self):
        """Test the ML-based similarity matching with new features."""
        result = self.recommender.find_similar_suppliers('S001', top_n=2)
        
        recommended_ids = [s['supplier_id'] for s in result.recommended_suppliers]
        
        # With geographic proximity, S004 and S006 might be closer to S001
        self.assertIn('S004', recommended_ids)
        self.assertIn('S006', recommended_ids)
        self.assertNotIn('S001', recommended_ids) # Should not recommend itself
        self.assertEqual(len(recommended_ids), 2)

    def test_find_similar_suppliers_invalid_id(self):
        """Test similarity search with an invalid supplier ID."""
        with self.assertRaises(ValueError):
            self.recommender.find_similar_suppliers('INVALID_ID')
            
    def test_collaborative_filtering_placeholder(self):
        """Test the collaborative filtering placeholder."""
        result = self.recommender.recommend_collaborative(user_id='test_user', top_n=3)
        
        # The placeholder returns top by ESG
        recommended_ids = [s['supplier_id'] for s in result.recommended_suppliers]
        self.assertEqual(recommended_ids, ['S006', 'S002', 'S004'])


if __name__ == '__main__':
    unittest.main()
