"""
API Endpoints for Transport Route Optimization
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import asyncio

from api.core.transport_optimizer import RouteOptimizer, RouteOptimizationAPI

router = APIRouter()
optimizer = RouteOptimizer()

class RouteRequest(BaseModel):
    """Request model for route optimization"""
    origin: str = Field(..., description="Origin location name")
    destination: str = Field(..., description="Destination location name")
    weight_tonnes: float = Field(1.0, gt=0, description="Shipment weight in tonnes")
    priority: str = Field("balanced", description="Optimization priority: carbon, cost, time, balanced")

class MultiRouteRequest(BaseModel):
    """Request model for multiple route comparison"""
    routes: List[RouteRequest] = Field(..., max_items=10)

@router.post("/optimize/route")
async def optimize_single_route(request: RouteRequest):
    """
    Get optimal transport routes for a single origin-destination pair
    """
    try:
        available_locations = list(optimizer.locations.keys())
        
        if request.origin not in available_locations:
            raise HTTPException(
                status_code=400, 
                detail=f"Origin '{request.origin}' not found. Available: {available_locations}"
            )
        
        if request.destination not in available_locations:
            raise HTTPException(
                status_code=400,
                detail=f"Destination '{request.destination}' not found. Available: {available_locations}"
            )
        
        routes = optimizer.find_optimal_routes(
            request.origin, 
            request.destination, 
            request.weight_tonnes, 
            request.priority
        )
        
        # Format response
        formatted_routes = []
        for route in routes:
            formatted_routes.append({
                "mode": route.mode.name,
                "distance_km": round(route.distance_km, 2),
                "emissions_kg_per_tonne": round(route.emissions_kg_per_tonne, 2),
                "cost_per_tonne": round(route.cost_per_tonne, 2),
                "transit_time_hours": round(route.transit_time_hours, 1),
                "carbon_tax_rate": route.carbon_tax_rate,
                "total_emissions_kg": round(route.emissions_kg_per_tonne * request.weight_tonnes, 2),
                "total_cost": round(route.cost_per_tonne * request.weight_tonnes, 2)
            })
        
        return {
            "origin": request.origin,
            "destination": request.destination,
            "weight_tonnes": request.weight_tonnes,
            "optimization_priority": request.priority,
            "routes": formatted_routes
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Route optimization failed: {str(e)}")

@router.post("/optimize/multimodal")
async def optimize_multimodal_routes(request: RouteRequest):
    """
    Find optimal multimodal routes using intermediate hubs
    """
    try:
        multimodal_routes = optimizer.find_multimodal_routes(
            request.origin,
            request.destination,
            request.weight_tonnes
        )
        
        return {
            "origin": request.origin,
            "destination": request.destination,
            "weight_tonnes": request.weight_tonnes,
            "multimodal_options": multimodal_routes
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multimodal optimization failed: {str(e)}")

@router.post("/optimize/carbon-savings")
async def calculate_carbon_savings(request: RouteRequest):
    """
    Calculate potential carbon savings by choosing optimal transport
    """
    try:
        savings_analysis = optimizer.calculate_carbon_savings(
            request.origin,
            request.destination,
            request.weight_tonnes
        )
        
        return {
            "origin": request.origin,
            "destination": request.destination,
            "weight_tonnes": request.weight_tonnes,
            "analysis": savings_analysis
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Carbon savings analysis failed: {str(e)}")

@router.get("/locations")
async def get_available_locations():
    """
    Get list of available locations for route optimization
    """
    locations = []
    for name, location in optimizer.locations.items():
        locations.append({
            "name": name,
            "country_code": location.country_code,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "port_type": location.port_type
        })
    
    return {
        "total_locations": len(locations),
        "locations": locations
    }

@router.post("/optimize/batch")
async def optimize_batch_routes(request: MultiRouteRequest):
    """
    Optimize multiple routes in a single request
    """
    try:
        results = []
        
        for route_req in request.routes:
            try:
                routes = optimizer.find_optimal_routes(
                    route_req.origin,
                    route_req.destination,
                    route_req.weight_tonnes,
                    route_req.priority
                )
                
                best_route = routes[0] if routes else None
                if best_route:
                    results.append({
                        "origin": route_req.origin,
                        "destination": route_req.destination,
                        "weight_tonnes": route_req.weight_tonnes,
                        "optimal_route": {
                            "mode": best_route.mode.name,
                            "emissions_kg": round(best_route.emissions_kg_per_tonne * route_req.weight_tonnes, 2),
                            "cost": round(best_route.cost_per_tonne * route_req.weight_tonnes, 2),
                            "time_hours": round(best_route.transit_time_hours, 1)
                        }
                    })
                else:
                    results.append({
                        "origin": route_req.origin,
                        "destination": route_req.destination,
                        "error": "No routes found"
                    })
            except Exception as e:
                results.append({
                    "origin": route_req.origin,
                    "destination": route_req.destination,
                    "error": str(e)
                })
        
        return {
            "batch_size": len(request.routes),
            "successful": len([r for r in results if "error" not in r]),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch optimization failed: {str(e)}")

@router.get("/carbon-tax-rates")
async def get_carbon_tax_rates():
    """
    Get current carbon tax rates by country
    """
    return {
        "carbon_tax_rates": optimizer.carbon_tax_rates,
        "currency": "USD per tonne CO2",
        "note": "Rates are simplified estimates for demonstration purposes"
    }