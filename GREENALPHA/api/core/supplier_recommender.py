"""
Core Supplier Recommendation Engine.

This module contains the logic for the supplier recommendation system, including
Multi-Criteria Decision Analysis (MCDA), machine learning-based similarity matching,
and a collaborative filtering approach.
"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from pydantic import BaseModel, Field
from typing import List, Dict

# Mock data for demonstration purposes
MOCK_SUPPLIER_DATA = {
    'supplier_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006'],
    'esg_score': [85, 92, 78, 88, 65, 95],
    'carbon_footprint': [120, 100, 150, 110, 200, 90], # in tCO2e
    'cost_index': [0.95, 1.05, 0.90, 1.00, 0.85, 1.10], # relative cost
    'reliability_score': [0.98, 0.95, 0.99, 0.96, 0.90, 0.99],
    'geographic_proximity': [0.9, 0.5, 0.8, 0.6, 0.3, 0.95], # normalized proximity score
    'compliance_status': [True, True, False, True, True, True],
    'product_category': ['Electronics', 'Electronics', 'Textiles', 'Electronics', 'Textiles', 'Electronics']
}
MOCK_SUPPLIERS_DF = pd.DataFrame(MOCK_SUPPLIER_DATA)

class Supplier(BaseModel):
    """Data model for a supplier."""
    supplier_id: str
    esg_score: float
    carbon_footprint: float
    cost_index: float
    reliability_score: float
    geographic_proximity: float
    compliance_status: bool
    product_category: str

class RecommendationResult(BaseModel):
    """Data model for a recommendation result."""
    recommended_suppliers: List[Dict] = Field(..., description="List of recommended suppliers with their scores.")
    
class SupplierRecommender:
    """
    Implements the supplier recommendation logic.
    """
    def __init__(self, suppliers_df: pd.DataFrame = MOCK_SUPPLIERS_DF):
        self.suppliers = suppliers_df.copy()
        self.scaler = MinMaxScaler()
        # Define features for ML similarity and MCDA
        self.features = ['esg_score', 'carbon_footprint', 'cost_index', 'reliability_score', 'geographic_proximity']
        self.scaled_features = self.scaler.fit_transform(self.suppliers[self.features])
        # Initialize Nearest Neighbors model for similarity matching
        self.nn_model = NearestNeighbors(n_neighbors=3, algorithm='ball_tree')
        self.nn_model.fit(self.scaled_features)

    def _mcda_score(self, weights: Dict[str, float]) -> pd.Series:
        """
        Calculates a weighted score for each supplier using MCDA.
        
        Args:
            weights (Dict[str, float]): A dictionary with weights for each criterion.
        
        Returns:
            pd.Series: A series with the calculated MCDA score for each supplier.
        """
        normalized_df = pd.DataFrame(self.scaler.fit_transform(self.suppliers[self.features]), 
                                     columns=self.features, 
                                     index=self.suppliers.index)
        
        # Apply weights
        weighted_scores = pd.Series(0.0, index=self.suppliers.index)
        
        # Metrics where higher is better
        for feature in ['esg_score', 'reliability_score', 'geographic_proximity']:
            weighted_scores += normalized_df[feature] * weights.get(feature, 0)
            
        # Metrics where lower is better
        for feature in ['carbon_footprint', 'cost_index']:
            weighted_scores += (1 - normalized_df[feature]) * weights.get(feature, 0)

        # Apply penalty for non-compliant suppliers
        penalty = 0.2 # 20% penalty
        weighted_scores[self.suppliers['compliance_status'] == False] *= (1 - penalty)

        return weighted_scores

    def recommend_by_mcda(self, weights: Dict[str, float], top_n: int = 3) -> RecommendationResult:
        """
        Recommends suppliers based on MCDA scores.
        """
        mcda_scores = self._mcda_score(weights)
        self.suppliers['mcda_score'] = mcda_scores
        
        # Get top N suppliers
        recommended = self.suppliers.sort_values(by='mcda_score', ascending=False).head(top_n)
        
        return RecommendationResult(recommended_suppliers=recommended.to_dict('records'))

    def find_similar_suppliers(self, supplier_id: str, top_n: int = 3) -> RecommendationResult:
        """
        Finds suppliers similar to a given supplier using ML.
        """
        if supplier_id not in self.suppliers['supplier_id'].values:
            raise ValueError("Supplier ID not found.")
            
        supplier_index = self.suppliers.index[self.suppliers['supplier_id'] == supplier_id][0]
        supplier_features = self.scaled_features[supplier_index].reshape(1, -1)
        
        distances, indices = self.nn_model.kneighbors(supplier_features, n_neighbors=top_n + 1)
        
        # Exclude the supplier itself from the results
        similar_suppliers_indices = [idx for idx in indices.flatten() if idx != supplier_index][:top_n]
        
        similar_suppliers = self.suppliers.iloc[similar_suppliers_indices]
        
        return RecommendationResult(recommended_suppliers=similar_suppliers.to_dict('records'))

    # Placeholder for collaborative filtering
    def recommend_collaborative(self, user_id: str, top_n: int = 3) -> RecommendationResult:
        """
        Placeholder for collaborative filtering recommendations.
        
        This would typically involve a user-item interaction matrix.
        """
        # For now, return top suppliers by ESG score as a placeholder
        top_by_esg = self.suppliers.sort_values(by='esg_score', ascending=False).head(top_n)
        return RecommendationResult(recommended_suppliers=top_by_esg.to_dict('records'))

# Example Usage:
if __name__ == '__main__':
    recommender = SupplierRecommender()

    # MCDA example with new criteria
    mcda_weights = {
        'esg_score': 0.40,           # 40%
        'cost_index': 0.30,          # 30%
        'reliability_score': 0.20,   # 20%
        'geographic_proximity': 0.10 # 10%
    }
    mcda_recommendations = recommender.recommend_by_mcda(mcda_weights)
    print("MCDA Recommendations:")
    for supplier in mcda_recommendations.recommended_suppliers:
        print(f"- Supplier: {supplier['supplier_id']}, Score: {supplier['mcda_score']:.4f}")

    # ML Similarity example
    similar_to_s001 = recommender.find_similar_suppliers('S001')
    print("\nSuppliers similar to S001:")
    for supplier in similar_to_s001.recommended_suppliers:
        print(f"- Supplier: {supplier['supplier_id']}")
