"""
Advanced Transport Route Optimization Engine
Optimizes shipping routes for minimal carbon footprint and cost
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from geopy.distance import geodesic
from pydantic import BaseModel
import math

class TransportMode(Enum):
    """Transport modes with emission factors"""
    SEA_FREIGHT = {"factor": 0.008, "cost_per_km": 0.05, "speed_kmh": 30}
    AIR_FREIGHT = {"factor": 1.1, "cost_per_km": 1.2, "speed_kmh": 900}
    RAIL_FREIGHT = {"factor": 0.022, "cost_per_km": 0.08, "speed_kmh": 80}
    ROAD_FREIGHT = {"factor": 0.089, "cost_per_km": 0.15, "speed_kmh": 65}
    INTERMODAL = {"factor": 0.015, "cost_per_km": 0.07, "speed_kmh": 45}

@dataclass
class Location:
    """Geographic location with coordinates"""
    name: str
    latitude: float
    longitude: float
    country_code: str
    port_type: str = "standard"  # standard, major_port, inland

@dataclass
class Route:
    """Transport route between two locations"""
    origin: Location
    destination: Location
    mode: TransportMode
    distance_km: float
    emissions_kg_per_tonne: float
    cost_per_tonne: float
    transit_time_hours: float
    carbon_tax_rate: float = 0.0
    
class RouteOptimizer:
    """
    Advanced route optimization for minimum carbon footprint and cost
    """
    
    def __init__(self):
        # Major global ports and logistics hubs
        self.locations = {
            'Shanghai': Location('Shanghai', 31.2304, 121.4737, 'CHN', 'major_port'),
            'Singapore': Location('Singapore', 1.3521, 103.8198, 'SGP', 'major_port'),
            'Rotterdam': Location('Rotterdam', 51.9244, 4.4777, 'NLD', 'major_port'),
            'Los Angeles': Location('Los Angeles', 34.0522, -118.2437, 'USA', 'major_port'),
            'Hong Kong': Location('Hong Kong', 22.3193, 114.1694, 'HKG', 'major_port'),
            'Hamburg': Location('Hamburg', 53.5511, 9.9937, 'DEU', 'major_port'),
            'Antwerp': Location('Antwerp', 51.2194, 4.4025, 'BEL', 'major_port'),
            'Dubai': Location('Dubai', 25.2048, 55.2708, 'ARE', 'major_port'),
            'New York': Location('New York', 40.7128, -74.0060, 'USA', 'major_port'),
            'Tokyo': Location('Tokyo', 35.6762, 139.6503, 'JPN', 'major_port'),
            'Mumbai': Location('Mumbai', 19.0760, 72.8777, 'IND', 'major_port'),
            'Guangzhou': Location('Guangzhou', 23.1291, 113.2644, 'CHN', 'standard'),
            'London': Location('London', 51.5074, -0.1278, 'GBR', 'standard'),
            'Frankfurt': Location('Frankfurt', 50.1109, 8.6821, 'DEU', 'standard'),
            'Chicago': Location('Chicago', 41.8781, -87.6298, 'USA', 'standard')
        }
        
        # Carbon tax rates by country ($/tonne CO2)
        self.carbon_tax_rates = {
            'CHN': 7, 'USA': 15, 'DEU': 25, 'GBR': 22, 'FRA': 30,
            'JPN': 3, 'SGP': 5, 'NLD': 28, 'BEL': 25, 'ARE': 0,
            'IND': 2, 'HKG': 0
        }
    
    def calculate_distance(self, origin: Location, destination: Location) -> float:
        """Calculate great circle distance between two locations"""
        return geodesic(
            (origin.latitude, origin.longitude),
            (destination.latitude, destination.longitude)
        ).kilometers
    
    def calculate_route_metrics(
        self, 
        origin: Location, 
        destination: Location, 
        mode: TransportMode,
        weight_tonnes: float = 1.0
    ) -> Route:
        """Calculate comprehensive route metrics"""
        
        distance = self.calculate_distance(origin, destination)
        mode_data = mode.value
        
        # Base emissions (kg CO2 per tonne-km)
        base_emissions = mode_data["factor"] * distance * weight_tonnes
        
        # Base cost
        base_cost = mode_data["cost_per_km"] * distance * weight_tonnes
        
        # Transit time
        transit_time = distance / mode_data["speed_kmh"]
        
        # Carbon tax calculation
        carbon_tax_rate = max(
            self.carbon_tax_rates.get(origin.country_code, 0),
            self.carbon_tax_rates.get(destination.country_code, 0)
        )
        carbon_tax_cost = (base_emissions / 1000) * carbon_tax_rate  # Convert kg to tonnes
        
        total_cost = base_cost + carbon_tax_cost
        
        return Route(
            origin=origin,
            destination=destination,
            mode=mode,
            distance_km=distance,
            emissions_kg_per_tonne=base_emissions / weight_tonnes,
            cost_per_tonne=total_cost / weight_tonnes,
            transit_time_hours=transit_time,
            carbon_tax_rate=carbon_tax_rate
        )
    
    def find_optimal_routes(
        self,
        origin_name: str,
        destination_name: str,
        weight_tonnes: float = 1.0,
        priority: str = "carbon"  # "carbon", "cost", "time", "balanced"
    ) -> List[Route]:
        """
        Find optimal routes based on different priorities
        """
        if origin_name not in self.locations or destination_name not in self.locations:
            raise ValueError(f"Unknown location. Available: {list(self.locations.keys())}")
        
        origin = self.locations[origin_name]
        destination = self.locations[destination_name]
        
        # Calculate routes for all transport modes
        routes = []
        for mode in TransportMode:
            route = self.calculate_route_metrics(origin, destination, mode, weight_tonnes)
            routes.append(route)
        
        # Sort based on priority
        if priority == "carbon":
            routes.sort(key=lambda r: r.emissions_kg_per_tonne)
        elif priority == "cost":
            routes.sort(key=lambda r: r.cost_per_tonne)
        elif priority == "time":
            routes.sort(key=lambda r: r.transit_time_hours)
        elif priority == "balanced":
            # Weighted scoring: 40% carbon, 35% cost, 25% time
            for route in routes:
                # Normalize metrics (0-1 scale)
                max_emissions = max(r.emissions_kg_per_tonne for r in routes)
                max_cost = max(r.cost_per_tonne for r in routes)
                max_time = max(r.transit_time_hours for r in routes)
                
                normalized_emissions = route.emissions_kg_per_tonne / max_emissions
                normalized_cost = route.cost_per_tonne / max_cost
                normalized_time = route.transit_time_hours / max_time
                
                route.balanced_score = (
                    0.40 * normalized_emissions +
                    0.35 * normalized_cost +
                    0.25 * normalized_time
                )
            
            routes.sort(key=lambda r: r.balanced_score)
        
        return routes
    
    def find_multimodal_routes(
        self,
        origin_name: str,
        destination_name: str,
        weight_tonnes: float = 1.0
    ) -> List[Dict]:
        """
        Find optimal multimodal routes using intermediate hubs
        """
        if origin_name not in self.locations or destination_name not in self.locations:
            raise ValueError(f"Unknown location. Available: {list(self.locations.keys())}")
        
        origin = self.locations[origin_name]
        destination = self.locations[destination_name]
        
        multimodal_routes = []
        
        # Consider major ports as intermediate hubs
        major_hubs = [loc for loc in self.locations.values() if loc.port_type == "major_port"]
        
        for hub in major_hubs:
            if hub.name in [origin_name, destination_name]:
                continue
                
            # Calculate route: Origin -> Hub -> Destination
            try:
                # Choose optimal mode for each leg
                leg1_routes = self.find_optimal_routes(origin_name, hub.name, weight_tonnes, "balanced")
                leg2_routes = self.find_optimal_routes(hub.name, destination_name, weight_tonnes, "balanced")
                
                if leg1_routes and leg2_routes:
                    best_leg1 = leg1_routes[0]
                    best_leg2 = leg2_routes[0]
                    
                    total_emissions = best_leg1.emissions_kg_per_tonne + best_leg2.emissions_kg_per_tonne
                    total_cost = best_leg1.cost_per_tonne + best_leg2.cost_per_tonne
                    total_time = best_leg1.transit_time_hours + best_leg2.transit_time_hours + 24  # 24h hub processing
                    total_distance = best_leg1.distance_km + best_leg2.distance_km
                    
                    multimodal_routes.append({
                        "route_type": "multimodal",
                        "hub": hub.name,
                        "leg1": {
                            "from": origin_name,
                            "to": hub.name,
                            "mode": best_leg1.mode.name,
                            "emissions": best_leg1.emissions_kg_per_tonne,
                            "cost": best_leg1.cost_per_tonne,
                            "time": best_leg1.transit_time_hours,
                            "distance": best_leg1.distance_km
                        },
                        "leg2": {
                            "from": hub.name,
                            "to": destination_name,
                            "mode": best_leg2.mode.name,
                            "emissions": best_leg2.emissions_kg_per_tonne,
                            "cost": best_leg2.cost_per_tonne,
                            "time": best_leg2.transit_time_hours,
                            "distance": best_leg2.distance_km
                        },
                        "totals": {
                            "emissions_kg_per_tonne": total_emissions,
                            "cost_per_tonne": total_cost,
                            "transit_time_hours": total_time,
                            "total_distance_km": total_distance
                        }
                    })
            except Exception:
                continue
        
        # Sort by total emissions
        multimodal_routes.sort(key=lambda r: r["totals"]["emissions_kg_per_tonne"])
        
        return multimodal_routes[:5]  # Return top 5 multimodal options
    
    def calculate_carbon_savings(
        self,
        origin_name: str,
        destination_name: str,
        weight_tonnes: float = 1.0
    ) -> Dict:
        """
        Calculate potential carbon savings by choosing optimal routes
        """
        routes = self.find_optimal_routes(origin_name, destination_name, weight_tonnes, "carbon")
        
        if len(routes) < 2:
            return {"savings": 0, "message": "Only one transport mode available"}
        
        best_route = routes[0]
        worst_route = routes[-1]
        
        emissions_saved = worst_route.emissions_kg_per_tonne - best_route.emissions_kg_per_tonne
        cost_difference = best_route.cost_per_tonne - worst_route.cost_per_tonne
        time_difference = best_route.transit_time_hours - worst_route.transit_time_hours
        
        # Calculate monetary value of carbon savings
        avg_carbon_price = 25  # $25/tonne CO2
        carbon_value = (emissions_saved / 1000) * avg_carbon_price  # Convert kg to tonnes
        
        return {
            "best_option": {
                "mode": best_route.mode.name,
                "emissions_kg": best_route.emissions_kg_per_tonne,
                "cost": best_route.cost_per_tonne,
                "time_hours": best_route.transit_time_hours
            },
            "worst_option": {
                "mode": worst_route.mode.name,
                "emissions_kg": worst_route.emissions_kg_per_tonne,
                "cost": worst_route.cost_per_tonne,
                "time_hours": worst_route.transit_time_hours
            },
            "savings": {
                "emissions_kg_saved": emissions_saved,
                "emissions_reduction_percent": (emissions_saved / worst_route.emissions_kg_per_tonne) * 100,
                "cost_difference": cost_difference,
                "time_difference_hours": time_difference,
                "carbon_credit_value": carbon_value
            }
        }

class RouteOptimizationAPI(BaseModel):
    """API models for route optimization"""
    origin: str
    destination: str
    weight_tonnes: float = 1.0
    priority: str = "balanced"

# Example usage and testing
if __name__ == "__main__":
    optimizer = RouteOptimizer()
    
    # Test route optimization
    routes = optimizer.find_optimal_routes("Shanghai", "Rotterdam", 10.0, "balanced")
    print("Optimal Routes (Shanghai to Rotterdam):")
    for i, route in enumerate(routes[:3]):
        print(f"{i+1}. {route.mode.name}: {route.emissions_kg_per_tonne:.2f} kg CO2/tonne, "
              f"${route.cost_per_tonne:.2f}/tonne, {route.transit_time_hours:.1f} hours")
    
    # Test carbon savings
    savings = optimizer.calculate_carbon_savings("Shanghai", "New York", 5.0)
    print(f"\nCarbon Savings Analysis:")
    print(f"Best: {savings['best_option']['mode']} - {savings['best_option']['emissions_kg']:.2f} kg CO2/tonne")
    print(f"Worst: {savings['worst_option']['mode']} - {savings['worst_option']['emissions_kg']:.2f} kg CO2/tonne")
    print(f"Savings: {savings['savings']['emissions_kg_saved']:.2f} kg CO2/tonne "
          f"({savings['savings']['emissions_reduction_percent']:.1f}%)")
    
    # Test multimodal routes
    multimodal = optimizer.find_multimodal_routes("Guangzhou", "Frankfurt", 2.0)
    print(f"\nTop Multimodal Routes:")
    for route in multimodal[:2]:
        print(f"Via {route['hub']}: {route['totals']['emissions_kg_per_tonne']:.2f} kg CO2/tonne, "
              f"${route['totals']['cost_per_tonne']:.2f}/tonne")