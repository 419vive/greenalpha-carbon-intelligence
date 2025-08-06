"""
API Endpoints for Supplier Recommendations.

This module defines the FastAPI routes for the supplier recommendation system.
"""
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import List, Dict

# Import the core recommender engine
from api.core.supplier_recommender import SupplierRecommender, RecommendationResult

router = APIRouter()
recommender = SupplierRecommender()

# --- Request and Response Models ---

class RecommendationRequest(BaseModel):
    """Request model for MCDA recommendations."""
    weights: Dict[str, float] = Field(..., example={
        'esg_score': 0.40,
        'cost_index': 0.30,
        'reliability_score': 0.20,
        'geographic_proximity': 0.10
    })
    top_n: int = Field(3, gt=0, le=10)
    page: int = Field(1, gt=0)
    page_size: int = Field(10, gt=0, le=100)

class PaginatedRecommendationResponse(BaseModel):
    """Paginated response model for recommendations."""
    total_suppliers: int
    page: int
    page_size: int
    total_pages: int
    items: List[Dict]

# --- API Endpoints ---

@router.post("/recommend/suppliers", response_model=PaginatedRecommendationResponse)
def get_supplier_recommendations(request: RecommendationRequest):
    """
    Get supplier recommendations based on Multi-Criteria Decision Analysis (MCDA).
    """
    try:
        # Note: In a real application, you'd apply pagination to a larger dataset
        # before scoring. For this mock implementation, we score all and then paginate.
        all_recommendations = recommender.recommend_by_mcda(request.weights, top_n=len(recommender.suppliers))
        
        # Paginate the results
        start_index = (request.page - 1) * request.page_size
        end_index = start_index + request.page_size
        paginated_items = all_recommendations.recommended_suppliers[start_index:end_index]

        total_items = len(all_recommendations.recommended_suppliers)
        total_pages = (total_items + request.page_size - 1) // request.page_size

        return PaginatedRecommendationResponse(
            total_suppliers=total_items,
            page=request.page,
            page_size=request.page_size,
            total_pages=total_pages,
            items=paginated_items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommend/alternatives/{supplier_id}", response_model=RecommendationResult)
def find_alternative_suppliers(supplier_id: str, top_n: int = 3):
    """
    Find alternative suppliers similar to a given supplier.
    """
    try:
        return recommender.find_similar_suppliers(supplier_id, top_n=top_n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend/batch", summary="Placeholder for Batch Recommendations")
def batch_recommendations(requests: List[RecommendationRequest]):
    """
    A placeholder endpoint for future bulk recommendation processing.
    
    In a real implementation, this would likely be an asynchronous task.
    """
    # For now, just return a confirmation
    return {"message": f"Received batch request for {len(requests)} recommendations. Processing not yet implemented."}
