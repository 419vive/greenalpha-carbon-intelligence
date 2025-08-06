"""
Carbon Footprint Calculation Methodology
Based on IPCC Guidelines and ISO 14067 standards
"""
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math
import time

class EmissionScope(Enum):
    """Carbon emission scopes according to GHG Protocol"""
    SCOPE_1 = "direct_emissions"  # Direct emissions from owned/controlled sources
    SCOPE_2 = "electricity_emissions"  # Indirect emissions from purchased electricity
    SCOPE_3 = "value_chain_emissions"  # All other indirect emissions

class TransportMode(Enum):
    """Transportation modes with their emission factors"""
    ROAD_TRUCK = "road_truck"
    RAIL = "rail"
    SEA_FREIGHT = "sea_freight"
    AIR_FREIGHT = "air_freight"
    PIPELINE = "pipeline"

@dataclass
class EmissionFactor:
    """Emission factor with metadata"""
    value: float  # kg CO2e per unit
    unit: str  # kg, km, kWh, etc.
    source: str  # Data source
    year: int  # Reference year
    uncertainty: float  # Uncertainty percentage
    region: Optional[str] = None

@dataclass
class ProductionData:
    """Product manufacturing data"""
    energy_intensity: float  # kWh per unit
    material_footprint: Dict[str, float]  # Material type -> kg CO2e per unit
    water_usage: float  # liters per unit
    waste_generation: float  # kg waste per unit

@dataclass
class TransportationData:
    """Transportation calculation data"""
    distance_km: float
    weight_kg: float
    mode: TransportMode
    fuel_efficiency: Optional[float] = None
    load_factor: float = 1.0  # Utilization factor

@dataclass
class CarbonFootprintResult:
    """Unified carbon footprint calculation result"""
    total_emissions: float  # kg CO2e
    production_emissions: float  # kg CO2e
    transport_emissions: float  # kg CO2e
    calculation_time_ms: float
    breakdown: Dict[str, float]
    uncertainty_percentage: float

class CarbonCalculationEngine:
    """
    Core carbon footprint calculation engine implementing IPCC methodologies
    """
    
    def __init__(self):
        self.emission_factors = self._initialize_emission_factors()
        self.country_factors = self._initialize_country_factors()
        self.transport_factors = self._initialize_transport_factors()
    
    def _initialize_emission_factors(self) -> Dict[str, EmissionFactor]:
        """Initialize standard emission factors"""
        return {
            # Energy sources (kg CO2e/kWh)
            "grid_electricity_global": EmissionFactor(0.475, "kWh", "IEA", 2021, 10.0),
            "natural_gas": EmissionFactor(0.202, "kWh", "IPCC", 2021, 5.0),
            "coal": EmissionFactor(0.820, "kWh", "IPCC", 2021, 8.0),
            "renewable": EmissionFactor(0.041, "kWh", "IPCC", 2021, 15.0),
            
            # Materials (kg CO2e/kg)
            "steel": EmissionFactor(2.3, "kg", "WorldSteel", 2021, 12.0),
            "aluminum": EmissionFactor(11.5, "kg", "IAI", 2021, 15.0),
            "concrete": EmissionFactor(0.5, "kg", "GCCA", 2021, 20.0),
            "plastic_pet": EmissionFactor(2.2, "kg", "PlasticsEurope", 2021, 18.0),
            "paper": EmissionFactor(0.9, "kg", "CEPI", 2021, 10.0),
            
            # Fuels (kg CO2e/L)
            "diesel": EmissionFactor(2.68, "L", "IPCC", 2021, 3.0),
            "gasoline": EmissionFactor(2.31, "L", "IPCC", 2021, 3.0),
            "jet_fuel": EmissionFactor(2.52, "L", "IPCC", 2021, 5.0),
        }
    
    def _initialize_country_factors(self) -> Dict[str, Dict[str, float]]:
        """Initialize country-specific emission factors"""
        return {
            "USA": {"electricity": 0.385, "energy_mix_factor": 1.0},
            "CHN": {"electricity": 0.644, "energy_mix_factor": 1.2},
            "DEU": {"electricity": 0.338, "energy_mix_factor": 0.9},
            "JPN": {"electricity": 0.462, "energy_mix_factor": 1.0},
            "IND": {"electricity": 0.708, "energy_mix_factor": 1.3},
            "BRA": {"electricity": 0.098, "energy_mix_factor": 0.7},
            "CAN": {"electricity": 0.110, "energy_mix_factor": 0.8},
        }
    
    def _initialize_transport_factors(self) -> Dict[TransportMode, EmissionFactor]:
        """Initialize transportation emission factors (kg CO2e/tonne-km)"""
        return {
            TransportMode.ROAD_TRUCK: EmissionFactor(0.062, "tonne-km", "IPCC", 2021, 20.0),
            TransportMode.RAIL: EmissionFactor(0.022, "tonne-km", "IPCC", 2021, 15.0),
            TransportMode.SEA_FREIGHT: EmissionFactor(0.014, "tonne-km", "IMO", 2021, 25.0),
            TransportMode.AIR_FREIGHT: EmissionFactor(0.602, "tonne-km", "ICAO", 2021, 30.0),
            TransportMode.PIPELINE: EmissionFactor(0.005, "tonne-km", "IPCC", 2021, 10.0),
        }
    
    def calculate_production_emissions(
        self, 
        product_data: ProductionData, 
        country_code: str,
        quantity: float = 1.0
    ) -> Dict[str, float]:
        """
        Calculate Scope 1 & 2 emissions from product manufacturing
        
        Formula: E = Σ(Activity_Data × Emission_Factor × Country_Factor)
        """
        country_factor = self.country_factors.get(country_code, {})
        electricity_factor = country_factor.get("electricity", 0.475)  # Global average
        energy_mix_factor = country_factor.get("energy_mix_factor", 1.0)
        
        # Energy emissions (Scope 2)
        energy_emissions = (
            product_data.energy_intensity * 
            electricity_factor * 
            energy_mix_factor * 
            quantity
        )
        
        # Material emissions (Scope 1 & 3)
        material_emissions = 0.0
        material_breakdown = {}
        
        for material, amount in product_data.material_footprint.items():
            if material in self.emission_factors:
                emission = amount * self.emission_factors[material].value * quantity
                material_emissions += emission
                material_breakdown[material] = emission
        
        # Process emissions (estimated based on energy intensity)
        process_emissions = energy_emissions * 0.15  # Typical ratio
        
        return {
            "total_production": energy_emissions + material_emissions + process_emissions,
            "energy_emissions": energy_emissions,
            "material_emissions": material_emissions,
            "process_emissions": process_emissions,
            "material_breakdown": material_breakdown,
            "uncertainty_percentage": self._calculate_uncertainty([
                product_data.energy_intensity,
                sum(product_data.material_footprint.values())
            ])
        }
    
    def calculate_transportation_emissions(
        self, 
        transport_data: TransportationData
    ) -> Dict[str, float]:
        """
        Calculate Scope 3 emissions from transportation
        
        Formula: E = Distance × Weight × Emission_Factor × Load_Factor
        """
        if transport_data.mode not in self.transport_factors:
            raise ValueError(f"Unsupported transport mode: {transport_data.mode}")
        
        emission_factor = self.transport_factors[transport_data.mode]
        
        # Convert weight to tonnes
        weight_tonnes = transport_data.weight_kg / 1000.0
        
        # Calculate base emissions
        base_emissions = (
            transport_data.distance_km * 
            weight_tonnes * 
            emission_factor.value * 
            transport_data.load_factor
        )
        
        # Apply mode-specific adjustments
        adjustment_factor = self._get_transport_adjustment(transport_data.mode)
        adjusted_emissions = base_emissions * adjustment_factor
        
        # Calculate additional factors
        upstream_emissions = adjusted_emissions * 0.2  # Fuel production
        infrastructure_emissions = adjusted_emissions * 0.05  # Infrastructure
        
        return {
            "total_transport": adjusted_emissions + upstream_emissions + infrastructure_emissions,
            "direct_transport": adjusted_emissions,
            "upstream_fuel": upstream_emissions,
            "infrastructure": infrastructure_emissions,
            "emission_factor_used": emission_factor.value,
            "uncertainty_percentage": emission_factor.uncertainty
        }
    
    def _get_transport_adjustment(self, mode: TransportMode) -> float:
        """Get transport mode specific adjustment factors"""
        adjustments = {
            TransportMode.ROAD_TRUCK: 1.0,
            TransportMode.RAIL: 0.8,  # Higher efficiency
            TransportMode.SEA_FREIGHT: 0.6,  # Most efficient for long distance
            TransportMode.AIR_FREIGHT: 1.5,  # Higher altitude effects
            TransportMode.PIPELINE: 0.7,  # Very efficient
        }
        return adjustments.get(mode, 1.0)
    
    def calculate_distance_great_circle(
        self, 
        lat1: float, lon1: float, 
        lat2: float, lon2: float
    ) -> float:
        """
        Calculate great circle distance between two points
        Using Haversine formula for accuracy
        """
        R = 6371  # Earth's radius in kilometers
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (math.sin(dlat/2)**2 + 
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def _calculate_uncertainty(self, values: List[float]) -> float:
        """Calculate combined uncertainty using error propagation"""
        if not values:
            return 0.0
        
        # Simplified uncertainty calculation (geometric mean)
        return math.sqrt(sum(v**2 for v in values if v > 0)) / len(values) * 100
    
    def get_emission_factor(self, factor_name: str) -> Optional[EmissionFactor]:
        """Get emission factor by name"""
        return self.emission_factors.get(factor_name)
    
    def update_emission_factor(self, name: str, factor: EmissionFactor):
        """Update or add emission factor"""
        self.emission_factors[name] = factor
    
    def calculate_footprint(
        self,
        production_data: ProductionData,
        transport_data: TransportationData,
        country_code: str = "USA",
        quantity: float = 1.0
    ) -> CarbonFootprintResult:
        """Unified carbon footprint calculation method"""
        start_time = time.time()
        
        try:
            # Calculate production emissions
            production_result = self.calculate_production_emissions(
                production_data, country_code, quantity
            )
            
            # Calculate transportation emissions
            transport_result = self.calculate_transportation_emissions(transport_data)
            
            # Extract numeric values from dictionaries
            production_emissions = production_result.get("total_production", 0.0)
            transport_emissions = transport_result.get("total_transport", 0.0)
            
            # Calculate total emissions
            total_emissions = production_emissions + transport_emissions
            
            # Calculate combined uncertainty
            prod_uncertainty = production_result.get("uncertainty_percentage", 15.0)
            transport_uncertainty = transport_result.get("uncertainty_percentage", 20.0)
            combined_uncertainty = (prod_uncertainty + transport_uncertainty) / 2
            
            # Create detailed breakdown
            breakdown = {
                "production_total": production_emissions,
                "transport_total": transport_emissions,
                **production_result,
                **transport_result
            }
            
            calculation_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return CarbonFootprintResult(
                total_emissions=total_emissions,
                production_emissions=production_emissions,
                transport_emissions=transport_emissions,
                calculation_time_ms=calculation_time,
                breakdown=breakdown,
                uncertainty_percentage=combined_uncertainty
            )
            
        except Exception as e:
            calculation_time = (time.time() - start_time) * 1000
            # Return error result with zero emissions but preserve timing
            return CarbonFootprintResult(
                total_emissions=0.0,
                production_emissions=0.0,
                transport_emissions=0.0,
                calculation_time_ms=calculation_time,
                breakdown={"error": str(e)},
                uncertainty_percentage=100.0
            )
    
    def calculate_product_footprint(
        self,
        product_name: str,
        quantity: float,
        origin: str,
        destination: str,
        transport_mode: str = "road_truck"
    ) -> CarbonFootprintResult:
        """Convenience method for calculating product footprint with minimal parameters"""
        # Product catalog lookup
        product_catalog = {
            "smartphone": ProductionData(
                energy_intensity=85.0,
                material_footprint={"steel": 0.025, "aluminum": 0.015, "plastic_pet": 0.08},
                water_usage=12000.0,
                waste_generation=0.5
            ),
            "laptop": ProductionData(
                energy_intensity=450.0,
                material_footprint={"steel": 0.15, "aluminum": 0.8, "plastic_pet": 0.3},
                water_usage=45000.0,
                waste_generation=2.1
            ),
        }
        
        # Get product data or use generic
        product_data = product_catalog.get(
            product_name.lower(),
            ProductionData(
                energy_intensity=200.0,
                material_footprint={"steel": 0.1, "aluminum": 0.05, "plastic_pet": 0.15},
                water_usage=25000.0,
                waste_generation=1.0
            )
        )
        
        # Calculate distance (simplified - using rough estimates)
        country_distances = {
            ("CHN", "USA"): 11000.0,
            ("USA", "CHN"): 11000.0,
            ("CHN", "DEU"): 7500.0,
            ("DEU", "CHN"): 7500.0,
            ("USA", "DEU"): 6500.0,
            ("DEU", "USA"): 6500.0,
        }
        
        distance = country_distances.get(
            (origin.upper(), destination.upper()),
            5000.0  # Default distance
        )
        
        # Estimate weight
        weight_estimates = {
            "smartphone": 0.2,
            "laptop": 2.5,
        }
        weight = weight_estimates.get(product_name.lower(), 1.0) * quantity
        
        # Create transport data
        transport_data = TransportationData(
            distance_km=distance,
            weight_kg=weight,
            mode=TransportMode(transport_mode),
            load_factor=0.8
        )
        
        return self.calculate_footprint(
            product_data, transport_data, origin, quantity
        )

# Global calculation engine instance
calculation_engine = CarbonCalculationEngine()