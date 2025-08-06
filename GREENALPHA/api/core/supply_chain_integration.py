"""
Supply Chain Data Integration Module
Integrates supply chain data for comprehensive carbon footprint analysis
"""
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Supplier:
    """Supplier information"""
    supplier_id: str
    name: str
    country: str
    city: str
    coordinates: Tuple[float, float]
    sustainability_rating: float  # 0-100
    carbon_intensity: float  # kg CO2e per unit
    certifications: List[str]
    reliability_score: float  # 0-100
    
@dataclass
class SupplyChainNode:
    """Supply chain node information"""
    node_id: str
    node_type: str  # supplier, manufacturer, distributor, retailer
    location: str
    carbon_emissions: float
    processing_time_days: float
    cost_usd: float
    
@dataclass
class SupplyChainRoute:
    """Complete supply chain route"""
    route_id: str
    nodes: List[SupplyChainNode]
    total_emissions: float
    total_cost: float
    total_time_days: float
    sustainability_score: float

class SupplyChainIntegrator:
    """Integrates and manages supply chain data"""
    
    def __init__(self):
        self.suppliers_db = self._load_suppliers_database()
        self.transport_networks = self._load_transport_networks()
        self.commodity_data = self._load_commodity_data()
        
    def _load_suppliers_database(self) -> Dict[str, Supplier]:
        """Load supplier database"""
        # Sample supplier data
        suppliers = {
            "SUP001": Supplier(
                supplier_id="SUP001",
                name="Green Materials Co",
                country="China",
                city="Shanghai",
                coordinates=(31.2304, 121.4737),
                sustainability_rating=85.0,
                carbon_intensity=2.5,
                certifications=["ISO14001", "B-Corp"],
                reliability_score=92.0
            ),
            "SUP002": Supplier(
                supplier_id="SUP002",
                name="EcoSteel Industries",
                country="Germany",
                city="Hamburg",
                coordinates=(53.5511, 9.9937),
                sustainability_rating=92.0,
                carbon_intensity=1.8,
                certifications=["ISO14001", "EU-Ecolabel", "Carbon-Neutral"],
                reliability_score=95.0
            ),
            "SUP003": Supplier(
                supplier_id="SUP003",
                name="Sustainable Textiles Ltd",
                country="India",
                city="Mumbai",
                coordinates=(19.0760, 72.8777),
                sustainability_rating=78.0,
                carbon_intensity=3.2,
                certifications=["GOTS", "Fair-Trade"],
                reliability_score=88.0
            ),
            "SUP004": Supplier(
                supplier_id="SUP004",
                name="CleanTech Metals",
                country="USA",
                city="Detroit",
                coordinates=(42.3314, -83.0458),
                sustainability_rating=88.0,
                carbon_intensity=2.1,
                certifications=["ISO14001", "Energy-Star"],
                reliability_score=94.0
            ),
            "SUP005": Supplier(
                supplier_id="SUP005",
                name="Nordic Bio Materials",
                country="Sweden",
                city="Stockholm",
                coordinates=(59.3293, 18.0686),
                sustainability_rating=95.0,
                carbon_intensity=1.2,
                certifications=["ISO14001", "Nordic-Swan", "Carbon-Negative"],
                reliability_score=97.0
            )
        }
        return suppliers
    
    def _load_transport_networks(self) -> Dict[str, Dict]:
        """Load transportation network data"""
        networks = {
            "maritime": {
                "routes": [
                    {"from": "Shanghai", "to": "Hamburg", "distance_km": 19000, "emissions_factor": 0.012},
                    {"from": "Mumbai", "to": "Hamburg", "distance_km": 11500, "emissions_factor": 0.013},
                    {"from": "Shanghai", "to": "Los Angeles", "distance_km": 10500, "emissions_factor": 0.011},
                ],
                "ports": ["Shanghai", "Hamburg", "Mumbai", "Los Angeles", "Singapore", "Rotterdam"]
            },
            "rail": {
                "routes": [
                    {"from": "Shanghai", "to": "Hamburg", "distance_km": 10800, "emissions_factor": 0.025},
                    {"from": "Detroit", "to": "Los Angeles", "distance_km": 3500, "emissions_factor": 0.023},
                ],
                "stations": ["Shanghai", "Hamburg", "Detroit", "Los Angeles", "Paris", "Moscow"]
            },
            "road": {
                "emissions_factor": 0.062,  # kg CO2e per ton-km
                "average_speed_kmh": 60
            },
            "air": {
                "emissions_factor": 0.602,  # kg CO2e per ton-km
                "average_speed_kmh": 800
            }
        }
        return networks
    
    def _load_commodity_data(self) -> pd.DataFrame:
        """Load commodity-specific data"""
        data = {
            "commodity": ["steel", "aluminum", "copper", "textiles", "electronics", "chemicals"],
            "production_emissions": [2.1, 11.9, 4.0, 5.5, 8.2, 3.8],  # kg CO2e per kg
            "processing_emissions": [0.5, 1.2, 0.8, 1.0, 2.1, 0.9],  # kg CO2e per kg
            "recycling_potential": [0.85, 0.95, 0.90, 0.60, 0.70, 0.40],  # percentage
            "waste_factor": [0.05, 0.03, 0.04, 0.10, 0.08, 0.07]  # percentage waste
        }
        return pd.DataFrame(data)
    
    def find_suppliers(self, 
                      product_category: str,
                      min_sustainability: float = 70.0,
                      max_carbon_intensity: float = 5.0) -> List[Supplier]:
        """Find suitable suppliers based on criteria"""
        suitable_suppliers = []
        for supplier in self.suppliers_db.values():
            if (supplier.sustainability_rating >= min_sustainability and
                supplier.carbon_intensity <= max_carbon_intensity):
                suitable_suppliers.append(supplier)
        
        # Sort by combination of sustainability and carbon intensity
        suitable_suppliers.sort(
            key=lambda s: (s.sustainability_rating / 100) * (1 / s.carbon_intensity),
            reverse=True
        )
        return suitable_suppliers
    
    def calculate_supply_chain_emissions(self,
                                        origin: str,
                                        destination: str,
                                        commodity: str,
                                        quantity_tons: float,
                                        transport_mode: str = "maritime") -> Dict:
        """Calculate complete supply chain emissions"""
        
        # Get commodity-specific factors
        commodity_factors = self.commodity_data[
            self.commodity_data['commodity'] == commodity.lower()
        ]
        
        if commodity_factors.empty:
            # Use default factors
            production_emissions = 3.0
            processing_emissions = 0.8
            waste_factor = 0.05
        else:
            production_emissions = commodity_factors['production_emissions'].values[0]
            processing_emissions = commodity_factors['processing_emissions'].values[0]
            waste_factor = commodity_factors['waste_factor'].values[0]
        
        # Calculate emissions for each stage
        quantity_with_waste = quantity_tons * (1 + waste_factor)
        
        # Production stage
        production_co2 = quantity_with_waste * production_emissions * 1000  # Convert to kg
        
        # Processing stage
        processing_co2 = quantity_with_waste * processing_emissions * 1000
        
        # Transportation stage
        transport_co2 = self._calculate_transport_emissions(
            origin, destination, quantity_with_waste, transport_mode
        )
        
        # Total emissions
        total_emissions = production_co2 + processing_co2 + transport_co2
        
        return {
            "total_emissions_kg_co2e": total_emissions,
            "production_emissions": production_co2,
            "processing_emissions": processing_co2,
            "transportation_emissions": transport_co2,
            "waste_adjusted_quantity": quantity_with_waste,
            "breakdown_percentage": {
                "production": (production_co2 / total_emissions) * 100,
                "processing": (processing_co2 / total_emissions) * 100,
                "transportation": (transport_co2 / total_emissions) * 100
            }
        }
    
    def _calculate_transport_emissions(self,
                                      origin: str,
                                      destination: str,
                                      quantity_tons: float,
                                      transport_mode: str) -> float:
        """Calculate transportation emissions"""
        # Simplified distance calculation (would use real routing in production)
        distance_km = self._estimate_distance(origin, destination, transport_mode)
        
        # Get emissions factor for transport mode
        if transport_mode in self.transport_networks:
            if transport_mode in ["maritime", "rail"]:
                # Check for specific route
                for route in self.transport_networks[transport_mode]["routes"]:
                    if (route["from"] == origin and route["to"] == destination) or \
                       (route["from"] == destination and route["to"] == origin):
                        emissions_factor = route["emissions_factor"]
                        distance_km = route["distance_km"]
                        break
                else:
                    # Use default factor
                    emissions_factor = 0.015 if transport_mode == "maritime" else 0.025
            else:
                emissions_factor = self.transport_networks[transport_mode]["emissions_factor"]
        else:
            emissions_factor = 0.062  # Default to road
        
        # Calculate emissions (ton-km * emissions factor)
        return quantity_tons * distance_km * emissions_factor
    
    def _estimate_distance(self, origin: str, destination: str, transport_mode: str) -> float:
        """Estimate distance between locations"""
        # Simplified distance estimates (would use real GIS data in production)
        distances = {
            ("Shanghai", "Hamburg"): {"maritime": 19000, "rail": 10800, "road": 12000, "air": 8900},
            ("Mumbai", "Hamburg"): {"maritime": 11500, "rail": 8500, "road": 9000, "air": 6500},
            ("Shanghai", "Los Angeles"): {"maritime": 10500, "air": 10000},
            ("Detroit", "Los Angeles"): {"rail": 3500, "road": 3300, "air": 3100},
            ("Stockholm", "Hamburg"): {"maritime": 1200, "rail": 1500, "road": 1300, "air": 1000},
        }
        
        # Check both directions
        key1 = (origin, destination)
        key2 = (destination, origin)
        
        if key1 in distances and transport_mode in distances[key1]:
            return distances[key1][transport_mode]
        elif key2 in distances and transport_mode in distances[key2]:
            return distances[key2][transport_mode]
        else:
            # Default distances by mode
            defaults = {"maritime": 10000, "rail": 5000, "road": 3000, "air": 2500}
            return defaults.get(transport_mode, 3000)
    
    def optimize_supply_chain(self,
                            origin: str,
                            destination: str,
                            commodity: str,
                            quantity_tons: float,
                            optimization_goal: str = "emissions") -> SupplyChainRoute:
        """Optimize supply chain route based on goal (emissions, cost, time)"""
        
        # Evaluate different transport modes
        modes = ["maritime", "rail", "road", "air"]
        routes = []
        
        for mode in modes:
            emissions_data = self.calculate_supply_chain_emissions(
                origin, destination, commodity, quantity_tons, mode
            )
            
            # Create route
            route = SupplyChainRoute(
                route_id=f"{origin}-{destination}-{mode}",
                nodes=[
                    SupplyChainNode(
                        node_id="origin",
                        node_type="supplier",
                        location=origin,
                        carbon_emissions=emissions_data["production_emissions"],
                        processing_time_days=2.0,
                        cost_usd=quantity_tons * 500  # Simplified cost
                    ),
                    SupplyChainNode(
                        node_id="transport",
                        node_type="transport",
                        location=f"{origin}-{destination}",
                        carbon_emissions=emissions_data["transportation_emissions"],
                        processing_time_days=self._estimate_transit_time(origin, destination, mode),
                        cost_usd=self._estimate_transport_cost(quantity_tons, mode)
                    ),
                    SupplyChainNode(
                        node_id="destination",
                        node_type="distributor",
                        location=destination,
                        carbon_emissions=emissions_data["processing_emissions"],
                        processing_time_days=1.0,
                        cost_usd=quantity_tons * 100
                    )
                ],
                total_emissions=emissions_data["total_emissions_kg_co2e"],
                total_cost=sum(node.cost_usd for node in []),
                total_time_days=sum(node.processing_time_days for node in []),
                sustainability_score=100 - (emissions_data["total_emissions_kg_co2e"] / (quantity_tons * 1000) * 10)
            )
            
            # Update totals
            route.total_cost = sum(node.cost_usd for node in route.nodes)
            route.total_time_days = sum(node.processing_time_days for node in route.nodes)
            
            routes.append(route)
        
        # Sort by optimization goal
        if optimization_goal == "emissions":
            routes.sort(key=lambda r: r.total_emissions)
        elif optimization_goal == "cost":
            routes.sort(key=lambda r: r.total_cost)
        elif optimization_goal == "time":
            routes.sort(key=lambda r: r.total_time_days)
        else:  # sustainability
            routes.sort(key=lambda r: r.sustainability_score, reverse=True)
        
        return routes[0]  # Return best route
    
    def _estimate_transit_time(self, origin: str, destination: str, mode: str) -> float:
        """Estimate transit time in days"""
        distance = self._estimate_distance(origin, destination, mode)
        speeds = {"maritime": 40, "rail": 80, "road": 60, "air": 800}  # km/h
        speed = speeds.get(mode, 60)
        return (distance / speed) / 24  # Convert hours to days
    
    def _estimate_transport_cost(self, quantity_tons: float, mode: str) -> float:
        """Estimate transportation cost"""
        cost_per_ton = {"maritime": 50, "rail": 80, "road": 120, "air": 500}
        return quantity_tons * cost_per_ton.get(mode, 100)
    
    def get_supplier_recommendations(self,
                                    commodity: str,
                                    destination: str,
                                    quantity_tons: float,
                                    max_results: int = 3) -> List[Dict]:
        """Get recommended suppliers with full supply chain analysis"""
        
        # Find suitable suppliers
        suppliers = self.find_suppliers(commodity, min_sustainability=75.0)[:max_results]
        
        recommendations = []
        for supplier in suppliers:
            # Calculate supply chain for this supplier
            emissions_data = self.calculate_supply_chain_emissions(
                supplier.city, destination, commodity, quantity_tons
            )
            
            # Optimize route
            best_route = self.optimize_supply_chain(
                supplier.city, destination, commodity, quantity_tons, "emissions"
            )
            
            recommendations.append({
                "supplier": asdict(supplier),
                "emissions_analysis": emissions_data,
                "optimized_route": {
                    "route_id": best_route.route_id,
                    "total_emissions": best_route.total_emissions,
                    "total_cost": best_route.total_cost,
                    "total_time_days": best_route.total_time_days,
                    "sustainability_score": best_route.sustainability_score
                },
                "recommendation_score": (
                    supplier.sustainability_rating * 0.4 +
                    supplier.reliability_score * 0.3 +
                    (100 - emissions_data["total_emissions_kg_co2e"] / (quantity_tons * 100)) * 0.3
                )
            })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda r: r["recommendation_score"], reverse=True)
        
        return recommendations