"""
Carbon Calculator API Routes
High-performance endpoints for carbon footprint calculations
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
import asyncio
import logging
from datetime import datetime

from api.core.carbon_engine import (
    carbon_engine,
    CarbonFootprintRequest,
    CarbonFootprintResult
)
from api.core.data_access import data_manager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["Carbon Calculator"])

# Request/Response Models
class CarbonCalculationRequest(BaseModel):
    """Carbon footprint calculation request model"""
    product_name: str = Field(..., description="Product name or category")
    quantity: float = Field(1.0, gt=0, description="Quantity of products")
    origin_country: str = Field(..., description="Origin country code (3-letter)")
    destination_country: str = Field(..., description="Destination country code (3-letter)")
    transport_mode: str = Field("road_truck", description="Transportation mode")
    product_category: Optional[str] = Field("general", description="Product category")
    weight_kg: Optional[float] = Field(None, gt=0, description="Total weight in kg")
    
    # Optional coordinates for precise distance calculation
    origin_latitude: Optional[float] = Field(None, ge=-90, le=90)
    origin_longitude: Optional[float] = Field(None, ge=-180, le=180)
    destination_latitude: Optional[float] = Field(None, ge=-90, le=90)
    destination_longitude: Optional[float] = Field(None, ge=-180, le=180)
    
    # Custom emission factors
    custom_emission_factors: Optional[Dict[str, float]] = Field(
        None, description="Custom emission factors override"
    )
    
    @field_validator('transport_mode')
    @classmethod
    def validate_transport_mode(cls, v):
        if not isinstance(v, str):
            raise ValueError('Transport mode must be a string')
        v = v.strip().lower()
        valid_modes = ['road_truck', 'rail', 'sea_freight', 'air_freight', 'pipeline']
        if v not in valid_modes:
            raise ValueError(f'Transport mode must be one of: {valid_modes}')
        return v
    
    @field_validator('origin_country', 'destination_country')
    @classmethod
    def validate_country_code(cls, v):
        if not isinstance(v, str):
            raise ValueError('Country code must be a string')
        v = v.strip().upper()
        if len(v) != 3:
            raise ValueError('Country code must be 3 letters (ISO 3166-1 alpha-3)')
        if not v.isalpha():
            raise ValueError('Country code must contain only letters')
        return v
    
    @field_validator('product_name')
    @classmethod
    def validate_product_name(cls, v):
        if not isinstance(v, str):
            raise ValueError('Product name must be a string')
        v = v.strip()
        if not v:
            raise ValueError('Product name cannot be empty')
        if len(v) > 100:
            raise ValueError('Product name too long (max 100 characters)')
        return v

class CarbonCalculationResponse(BaseModel):
    """Carbon footprint calculation response model"""
    # Core results
    total_emissions_kg_co2e: float
    production_emissions: float
    transportation_emissions: float
    
    # Scope breakdown
    scope_1_emissions: float
    scope_2_emissions: float  
    scope_3_emissions: float
    
    # Economic impact
    carbon_cost_usd: float
    carbon_trading_opportunities: List[Dict[str, Any]]
    
    # Metadata
    calculation_confidence: float
    response_time_ms: float
    calculation_method: str
    data_sources: List[str]
    
    # Detailed analysis
    production_breakdown: Dict[str, Any]
    transport_breakdown: Dict[str, Any]
    uncertainty_analysis: Dict[str, float]
    
    # Recommendations
    recommendations: Optional[List[Dict[str, str]]] = None

class BatchCalculationRequest(BaseModel):
    """Batch carbon footprint calculation request"""
    calculations: List[CarbonCalculationRequest] = Field(
        ..., max_items=100, description="List of calculations (max 100)"
    )
    include_summary: bool = Field(True, description="Include batch summary")

# Main calculation endpoint
@router.post("/calculate", response_model=CarbonCalculationResponse)
async def calculate_carbon_footprint(request: CarbonCalculationRequest):
    """
    Calculate carbon footprint for a product shipment
    
    This endpoint calculates the complete carbon footprint including:
    - Production emissions (Scope 1 & 2)
    - Transportation emissions (Scope 3)
    - Carbon cost estimation
    - Trading opportunities
    - Detailed breakdown and uncertainty analysis
    
    Response time target: <500ms for 95% of requests
    """
    try:
        # Convert to internal request format
        origin_coords = None
        dest_coords = None
        
        if (request.origin_latitude is not None and 
            request.origin_longitude is not None):
            origin_coords = (request.origin_latitude, request.origin_longitude)
            
        if (request.destination_latitude is not None and 
            request.destination_longitude is not None):
            dest_coords = (request.destination_latitude, request.destination_longitude)
        
        internal_request = CarbonFootprintRequest(
            product_name=request.product_name,
            quantity=request.quantity,
            origin_country=request.origin_country,
            destination_country=request.destination_country,
            origin_coordinates=origin_coords,
            destination_coordinates=dest_coords,
            transport_mode=request.transport_mode,
            product_category=request.product_category,
            weight_kg=request.weight_kg,
            custom_emission_factors=request.custom_emission_factors
        )
        
        # Perform calculation
        result = await carbon_engine.calculate_carbon_footprint(internal_request)
        
        # Generate recommendations
        recommendations = await _generate_recommendations(result, internal_request)
        
        # Convert to response format
        response = CarbonCalculationResponse(
            total_emissions_kg_co2e=result.total_emissions_kg_co2e,
            production_emissions=result.production_emissions,
            transportation_emissions=result.transportation_emissions,
            scope_1_emissions=result.scope_1_emissions,
            scope_2_emissions=result.scope_2_emissions,
            scope_3_emissions=result.scope_3_emissions,
            carbon_cost_usd=result.carbon_cost_usd,
            carbon_trading_opportunities=result.carbon_trading_opportunities,
            calculation_confidence=result.calculation_confidence,
            response_time_ms=result.response_time_ms,
            calculation_method=result.calculation_method,
            data_sources=result.data_sources,
            production_breakdown=result.production_breakdown,
            transport_breakdown=result.transport_breakdown,
            uncertainty_analysis=result.uncertainty_analysis,
            recommendations=recommendations
        )
        
        logger.info(
            f"Carbon calculation completed: {result.total_emissions_kg_co2e:.2f} kg CO2e "
            f"in {result.response_time_ms:.2f}ms"
        )
        
        return response
        
    except ValueError as e:
        logger.error(f"Invalid input for carbon calculation: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable - data not accessible")
    except Exception as e:
        logger.error(f"Carbon calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error during calculation")

@router.post("/calculate/batch")
async def calculate_batch_carbon_footprint(request: BatchCalculationRequest):
    """
    Calculate carbon footprint for multiple products in batch
    
    Processes up to 100 calculations in parallel for optimal performance.
    Returns individual results plus optional batch summary.
    """
    try:
        if len(request.calculations) > 100:
            raise HTTPException(
                status_code=400, 
                detail="Maximum 100 calculations per batch"
            )
        
        start_time = datetime.now()
        
        # Process calculations in parallel
        tasks = [
            calculate_carbon_footprint(calc_request)
            for calc_request in request.calculations
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Separate successful results from errors
        successful_results = []
        errors = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append({
                    "index": i,
                    "error": str(result),
                    "request": request.calculations[i].dict()
                })
            else:
                successful_results.append({
                    "index": i,
                    "result": result.dict() if hasattr(result, 'dict') else result
                })
        
        # Calculate batch summary
        batch_summary = None
        if request.include_summary and successful_results:
            batch_summary = _calculate_batch_summary(successful_results)
        
        total_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "batch_id": f"batch_{int(datetime.now().timestamp())}",
            "total_calculations": len(request.calculations),
            "successful_calculations": len(successful_results),
            "failed_calculations": len(errors),
            "batch_processing_time_ms": total_time,
            "results": successful_results,
            "errors": errors,
            "summary": batch_summary
        }
        
    except Exception as e:
        logger.error(f"Batch calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch calculation failed: {str(e)}")

@router.get("/factors/emission")
async def get_emission_factors():
    """Get available emission factors and their sources"""
    try:
        factors = carbon_engine.calc_engine.emission_factors
        
        return {
            "emission_factors": {
                name: {
                    "value": factor.value,
                    "unit": factor.unit,
                    "source": factor.source,
                    "year": factor.year,
                    "uncertainty": factor.uncertainty,
                    "region": factor.region
                }
                for name, factor in factors.items()
            },
            "total_factors": len(factors),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get emission factors: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve emission factors")

@router.get("/factors/country/{country_code}")
async def get_country_factors(country_code: str):
    """Get country-specific emission factors"""
    try:
        country_code = country_code.upper()
        
        # Get country profile
        profile = await data_manager.get_country_profile(country_code)
        if not profile:
            raise HTTPException(status_code=404, detail=f"Country {country_code} not found")
        
        # Get country-specific factors
        country_factors = carbon_engine.calc_engine.country_factors.get(country_code, {})
        
        return {
            "country_code": country_code,
            "country_name": profile.name,
            "electricity_factor": profile.electricity_factor,
            "energy_mix": profile.energy_mix,
            "total_emissions": profile.total_emissions,
            "per_capita_emissions": profile.per_capita_emissions,
            "latest_year": profile.latest_year,
            "additional_factors": country_factors
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get country factors: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve country factors")

@router.get("/transport/modes")
async def get_transport_modes():
    """Get available transportation modes and their emission factors"""
    try:
        transport_factors = carbon_engine.calc_engine.transport_factors
        
        return {
            "transport_modes": {
                mode.value: {
                    "emission_factor": factor.value,
                    "unit": factor.unit,
                    "source": factor.source,
                    "year": factor.year,
                    "uncertainty": factor.uncertainty,
                    "description": _get_transport_description(mode.value)
                }
                for mode, factor in transport_factors.items()
            },
            "total_modes": len(transport_factors)
        }
        
    except Exception as e:
        logger.error(f"Failed to get transport modes: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve transport modes")

@router.get("/products/catalog")
async def get_product_catalog():
    """Get available products in the catalog"""
    try:
        catalog = carbon_engine.product_catalog.products
        
        return {
            "products": {
                name: {
                    "energy_intensity": data.energy_intensity,
                    "material_footprint": data.material_footprint,
                    "water_usage": data.water_usage,
                    "waste_generation": data.waste_generation
                }
                for name, data in catalog.items()
            },
            "total_products": len(catalog),
            "supported_categories": list(set(
                product.split('_')[0] for product in catalog.keys()
            ))
        }
        
    except Exception as e:
        logger.error(f"Failed to get product catalog: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve product catalog")

@router.get("/countries/search")
async def search_countries(
    query: str = Query(..., description="Search query for country name or code"),
    limit: int = Query(20, le=100, description="Maximum results to return")
):
    """Search for countries by name or code"""
    try:
        results = await data_manager.search_countries(query)
        return {
            "query": query,
            "results": results[:limit],
            "total_found": len(results)
        }
        
    except Exception as e:
        logger.error(f"Country search failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Country search failed")

@router.get("/countries/{country_code}/emissions")
async def get_country_emissions(
    country_code: str,
    start_year: Optional[int] = Query(None, description="Start year for data"),
    end_year: Optional[int] = Query(None, description="End year for data")
):
    """Get historical emissions data for a country"""
    try:
        country_code = country_code.upper()
        
        emissions_history = await data_manager.get_emissions_history(
            country_code, start_year, end_year
        )
        
        if not emissions_history:
            raise HTTPException(
                status_code=404, 
                detail=f"No emissions data found for {country_code}"
            )
        
        return {
            "country_code": country_code,
            "data_points": len(emissions_history),
            "year_range": f"{min(dp.year for dp in emissions_history)}-{max(dp.year for dp in emissions_history)}",
            "emissions_history": [
                {
                    "year": dp.year,
                    "emissions_tonnes": dp.emissions_tonnes,
                    "entity": dp.entity
                }
                for dp in emissions_history
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get country emissions: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve emissions data")

@router.get("/stats/global")
async def get_global_statistics():
    """Get global carbon emission statistics"""
    try:
        stats = await data_manager.get_global_statistics()
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get global statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve global statistics")

@router.get("/stats/performance")
async def get_performance_statistics():
    """Get API and engine performance statistics"""
    try:
        engine_stats = carbon_engine.get_performance_stats()
        data_stats = data_manager.get_performance_stats()
        
        return {
            "engine_performance": engine_stats,
            "data_manager_performance": data_stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get performance stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve performance statistics")

# Helper functions
async def _generate_recommendations(
    result: CarbonFootprintResult, 
    request: CarbonFootprintRequest
) -> List[Dict[str, str]]:
    """Generate carbon reduction recommendations"""
    recommendations = []
    
    # Transport recommendations
    if result.transportation_emissions > result.production_emissions * 0.5:
        if request.transport_mode == "air_freight":
            recommendations.append({
                "category": "Transportation",
                "action": "Consider sea freight instead of air freight",
                "potential_reduction": "Up to 95% transport emissions",
                "priority": "High"
            })
        elif request.transport_mode == "road_truck":
            recommendations.append({
                "category": "Transportation", 
                "action": "Consider rail transport for long distances",
                "potential_reduction": "Up to 65% transport emissions",
                "priority": "Medium"
            })
    
    # Production recommendations
    if result.scope_2_emissions > result.scope_1_emissions:
        recommendations.append({
            "category": "Production",
            "action": "Source from countries with cleaner electricity grids",
            "potential_reduction": "10-50% production emissions",
            "priority": "Medium"
        })
    
    # General recommendations
    if result.total_emissions_kg_co2e > 100:  # High emissions
        recommendations.append({
            "category": "General",
            "action": "Consider carbon offset programs",
            "potential_reduction": "Net zero emissions",
            "priority": "Low"
        })
    
    return recommendations

def _calculate_batch_summary(successful_results: List[Dict]) -> Dict[str, Any]:
    """Calculate summary statistics for batch results"""
    if not successful_results:
        return {}
    
    emissions = [r["result"]["total_emissions_kg_co2e"] for r in successful_results]
    costs = [r["result"]["carbon_cost_usd"] for r in successful_results]
    
    return {
        "total_emissions_kg_co2e": sum(emissions),
        "average_emissions_kg_co2e": sum(emissions) / len(emissions),
        "min_emissions_kg_co2e": min(emissions),
        "max_emissions_kg_co2e": max(emissions),
        "total_carbon_cost_usd": sum(costs),
        "average_carbon_cost_usd": sum(costs) / len(costs),
        "calculations_processed": len(successful_results)
    }

def _get_transport_description(mode: str) -> str:
    """Get description for transport mode"""
    descriptions = {
        "road_truck": "Road freight transport by truck",
        "rail": "Railway freight transport",
        "sea_freight": "Ocean/sea freight transport",
        "air_freight": "Air cargo transport",
        "pipeline": "Pipeline transport (oil, gas, etc.)"
    }
    return descriptions.get(mode, "Unknown transport mode")