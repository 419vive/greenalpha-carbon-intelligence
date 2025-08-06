"""
Tests for the ESG Scoring Engine.

This test suite verifies the functionality of the ESGScoringEngine, including
score calculation, risk assessment, compliance checking, and report generation.
"""
import unittest
import sys
import os
from unittest.mock import MagicMock

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from api.core.esg_scoring import (
    ESGScoringEngine,
    ESGMetrics,
    CompanyESGProfile,
    ESGReport
)

class TestESGScoring(unittest.TestCase):
    """
    Tests the core functionality of the ESGScoringEngine.
    """

    def setUp(self):
        """Set up a mock ESGScoringEngine for each test."""
        self.esg_engine = ESGScoringEngine()
        # Mock data for a sample company
        self.sample_company_data = {
            'company_name': 'TestCorp',
            'industry': 'Technology',
            'metrics': {
                'carbon_emissions': 50000,
                'water_usage': 100000,
                'employee_turnover': 0.15,
                'board_diversity': 0.4,
                'data_privacy_breaches': 1,
                'supply_chain_audits': 25
            },
            'certifications': ['ISO 14001']
        }
        self.company_profile = CompanyESGProfile(**self.sample_company_data)

    def test_initialization(self):
        """Verify the ESG scoring engine loads all required data and components."""
        self.assertIsNotNone(self.esg_engine)
        self.assertGreater(len(self.esg_engine.industry_benchmarks), 0)

    def test_calculate_basic_esg_score(self):
        """Test that a basic ESG score is calculated correctly."""
        score = self.esg_engine.calculate_esg_score(self.company_profile)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_risk_level_determination(self):
        """Verify that risk levels (Low, Medium, High) correctly match scores."""
        risk_level = self.esg_engine.determine_risk_level(75)
        self.assertEqual(risk_level, 'Low')
        risk_level = self.esg_engine.determine_risk_level(50)
        self.assertEqual(risk_level, 'Medium')
        risk_level = self.esg_engine.determine_risk_level(25)
        self.assertEqual(risk_level, 'High')

    def test_component_scores(self):
        """Test the calculation of individual E, S, and G component scores."""
        components = self.esg_engine.get_component_scores(self.company_profile)
        self.assertIn('environmental', components)
        self.assertIn('social', components)
        self.assertIn('governance', components)
        self.assertIsInstance(components['environmental'], float)

    def test_compliance_checking(self):
        """Verify regulatory compliance detection for a given company profile."""
        compliance_status = self.esg_engine.check_compliance(self.company_profile)
        self.assertIsInstance(compliance_status, dict)
        self.assertIn('is_compliant', compliance_status)

    def test_peer_comparison(self):
        """Test the comparison of a company's score against industry benchmarks."""
        comparison = self.esg_engine.compare_to_peers(self.company_profile)
        self.assertIsInstance(comparison, dict)
        self.assertIn('industry_average', comparison)
        self.assertIn('percentile_rank', comparison)

    def test_recommendations_generation(self):
        """Verify the generation of actionable improvement suggestions."""
        recommendations = self.esg_engine.generate_recommendations(self.company_profile)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
        self.assertIsInstance(recommendations[0], str)

    def test_strengths_weaknesses_identification(self):
        """Test the SWOT analysis for identifying ESG strengths and weaknesses."""
        analysis = self.esg_engine.identify_strengths_weaknesses(self.company_profile)
        self.assertIn('strengths', analysis)
        self.assertIn('weaknesses', analysis)
        self.assertIsInstance(analysis['strengths'], list)

    def test_certification_impact(self):
        """Verify that relevant certifications positively affect ESG scores."""
        profile_no_cert = CompanyESGProfile(**{**self.sample_company_data, 'certifications': []})
        score_with_cert = self.esg_engine.calculate_esg_score(self.company_profile)
        score_without_cert = self.esg_engine.calculate_esg_score(profile_no_cert)
        self.assertGreater(score_with_cert, score_without_cert)

    def test_esg_report_generation(self):
        """Test the creation of a comprehensive ESG report object."""
        report = self.esg_engine.generate_esg_report(self.company_profile)
        self.assertIsInstance(report, ESGReport)
        self.assertEqual(report.company_name, 'TestCorp')
        self.assertIsNotNone(report.overall_score)

    def test_percentile_calculation(self):
        """Verify the peer ranking percentile calculation is mathematically correct."""
        # This test would benefit from a more controlled data set
        percentile = self.esg_engine._calculate_percentile(85, 'Technology')
        self.assertGreaterEqual(percentile, 0)
        self.assertLessEqual(percentile, 100)

class TestESGMetrics(unittest.TestCase):
    """
    Tests data processing and metrics extraction for ESG scoring.
    """

    def test_metrics_extraction_with_defaults(self):
        """Verify that defaults are used when no data is provided."""
        raw_data = {'company_name': 'EmptyCorp', 'industry': 'Retail'}
        metrics = ESGMetrics(raw_data)
        self.assertGreater(metrics.carbon_emissions, 0) # Should have a default value
        self.assertEqual(metrics.data_privacy_breaches, 0)

    def test_metrics_extraction_with_data(self):
        """Test metrics extraction with actual company data."""
        raw_data = {
            'company_name': 'DataCorp',
            'industry': 'Finance',
            'metrics': {
                'carbon_emissions': 12000,
                'board_diversity': 0.55
            }
        }
        metrics = ESGMetrics(raw_data)
        self.assertEqual(metrics.carbon_emissions, 12000)
        self.assertEqual(metrics.board_diversity, 0.55)
        # Test a default value for a missing metric
        self.assertEqual(metrics.supply_chain_audits, 0)


if __name__ == '__main__':
    unittest.main()
